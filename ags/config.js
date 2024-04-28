const Hyprland = await Service.import('hyprland')
const Mpris = await Service.import('mpris')
const Audio = await Service.import('audio')
const { Button, Box, CenterBox, Icon, Label, Revealer, Window } = Widget

const speakerRevealerState = Variable(false)
const microphoneRevealerState = Variable(false)

const cacheRevealerState = Variable(false)
const cacheButtonLock = Variable(false)

const tempsRevealerState = Variable(false)
const tempsButtonLock = Variable(false)

const percentagesRevealerState = Variable(false)
const percentagesButtonLock = Variable(false)

const isUnwantedSinkSelected = Variable(false)
const unwantedSink = 'iec958'

const category = {
    99: 'overamplified',
    66: 'high',
    33: 'medium',
    1: 'low',
    0: 'muted'
}
const sensors = Variable('', {
    poll: [1000, 'sensors -j', out => JSON.parse(out)]
})

const cpu = Variable('', {
    poll: [1000, ['bash', '-c', "top -bn 1 | grep '%Cpu' | awk '{print 100-$8}'"], value => `${Math.round(value)}%`]
})

const ram = Variable('', {
    poll: [1000, ['bash', '-c', "free | grep Mem: | awk '{print $3/$2 * 100}'"], value => `${Math.round(value)}%`]
})


const audioOutputSwitch = () => Button({
    onClicked: () => Audio.speaker = Audio.speakers.find(sink => {return sink.stream !== Audio.speaker.stream}),
    onMiddleClick: () => console.log(sensors.value),
    child: Icon().hook(Audio.speaker, self => {
        if (Audio.speaker.name?.includes('hdmi')) {
            self.icon = "video-display-symbolic"
            self.size = 12
        } else if (Audio.speaker.name?.includes('analog')) {
            self.icon = "audio-headphones-symbolic"
            self.size = 14
        } 
    }),
})

const staticWorkspaces = () => Box({
    children: [1,2,3,4,5,6,7,8,9,10].map(numb=>Button({
        onClicked: () => Hyprland.messageAsync(`dispatch workspace ${numb}`),
        child: Label(`${numb}`),
    }))
})

const Workspaces = () => Box({
    children: Hyprland.bind('workspaces').transform(ws => {
        return ws.sort((a, b) => a.id - b.id).map(({ id }) => Button({
            onClicked: () => Hyprland.messageAsync(`dispatch workspace ${id}`),
            child: Label(`${id}`),
            //className: Hyprland.active.workspace.bind('id').transform(i => `${i === id ? 'focused' : ''}`),
        }))
    }),
})

const Clock = () => Label({
    setup: self => self.poll(1000, self => Utils.execAsync(['date', '+%H:%M']).then(date => self.label = date)),
})

const cache = () => Button({
    onClicked: () => cacheButtonLock.value = !cacheButtonLock.value,
    child: Box({
        children: [
            Icon({className: 'revealerIcon', icon: cacheButtonLock.bind().as(value => value ? 'lock-symbolic' : 'drive-removable-media-symbolic')}),
            Revealer({
                reveal_child: cacheRevealerState.bind(),
                child: Label({
                    className: "revealerLabel",
                    setup: self => self.poll(1000, self => Utils.execAsync(['bash', '-c', "grep Dirty: /proc/meminfo | awk '{print $2$3}'"]).then(cacheinfo => self.label = cacheinfo))
                }),
                transition: 'slide_left',
            })
        ]
    })
})
.on("enter-notify-event", () => cacheRevealerState.value = true)
.on("leave-notify-event", () => {if (!cacheButtonLock.value) {cacheRevealerState.value = false}})


const temps = () => Button({
    onClicked: () => tempsButtonLock.value = !tempsButtonLock.value,
    child: Box({
        children: [
            Revealer({
                reveal_child: tempsRevealerState.bind(),
                child: Box({
                    children: [
                        Icon({icon: 'cpu-symbolic'}),
                        Label({
                            className: "revealerLabel",
                            label: sensors.bind().as(value => `${value["coretemp-isa-0000"]["Package id 0"]["temp1_input"]} °C`)})
                        ]
                }),
                transition: 'slide_left',
            }),
            Icon({className: 'revealerIcon', icon: tempsButtonLock.bind().as(value => value ? 'lock-symbolic' : 'temp-symbolic'),}),
            Revealer({
                reveal_child: tempsRevealerState.bind(),
                child: Box({
                    children: [
                        Label({
                            className: "revealerLabel",
                            label: sensors.bind().as(value => `${value["amdgpu-pci-0300"]["junction"]["temp2_input"]} °C`)}),
                        Icon({icon: 'freon-gpu-temperature-symbolic'})
                    ]
                }),
                transition: 'slide_right',
            }),
            
        ]
    })
})
.on("enter-notify-event", () => tempsRevealerState.value = true)
.on("leave-notify-event", () => {if (!tempsButtonLock.value) {tempsRevealerState.value = false}})

const percentages = () => Button({
    onClicked: () => percentagesButtonLock.value = !percentagesButtonLock.value,
    child: Box({
        children: [
            Revealer({
                reveal_child: percentagesRevealerState.bind(),
                child: Box({
                    children: [
                        Icon({icon: 'cpu-symbolic'}),
                        Label({
                            className: "revealerLabel",
                            label: cpu.bind()})
                        ]
                }),
                transition: 'slide_left',
            }),
            Icon({className: 'revealerIcon', icon: percentagesButtonLock.bind().as(value => value ? 'lock-symbolic' : 'temp-symbolic'),}),
            Revealer({
                reveal_child: percentagesRevealerState.bind(),
                child: Box({
                    children: [
                        Label({
                            className: "revealerLabel",
                            label: ram.bind()}),
                        Icon({icon: 'freon-gpu-temperature-symbolic'})
                    ]
                }),
                transition: 'slide_right',
            }),
            
        ]
    })
})
.on("enter-notify-event", () => percentagesRevealerState.value = true)
.on("leave-notify-event", () => {if (!percentagesButtonLock.value) {percentagesRevealerState.value = false}})



const nowPlaying = () => Button({
    onClicked: () => Mpris.getPlayer()?.playPause(),
    on_scroll_up: () => Mpris.getPlayer()?.next(),
    on_scroll_down: () => Mpris.getPlayer()?.previous(),
    onMiddleClick: () => Mpris.getPlayer()?.stop(),
    child: Label('-').hook(Mpris, self => {
        if (Mpris.players[0]) {
            const {track_artists, track_title, track_album} = Mpris.players[0]
            if (track_album) { // if its jellyfin
                self.label = `${track_artists.join(', ')} - ${track_title}`
            } else if (track_artists[0].includes(' - Topic')) { // if its youtube and artist/channel name has "topic"
                self.label = `${track_artists.join(', ').replace(' - Topic', '')} - ${track_title}`
            } else {
                self.label = track_title
            }
        } else {
            self.label = 'Nothing is playing'
        }
    }, 'player-changed'),
})

const speakerVolume = () => Button({
    on_scroll_up: () => {if (!isUnwantedSinkSelected.value) {Audio.speaker.volume < 0.9 ? Audio.speaker.volume += 0.1 : Audio.speaker.volume = 1}},
    on_scroll_down: () => {if (!isUnwantedSinkSelected.value) {Audio.speaker.volume -= 0.1}},
    onClicked: () => Utils.execAsync(['pactl', 'set-sink-mute', '@DEFAULT_SINK@', 'toggle']),
	child: Box({
        children: [
            Icon({className: 'revealerIcon'}).hook(Audio.speaker, self => {
                isUnwantedSinkSelected.value = Audio.speaker.name?.includes(unwantedSink)
                const icon = Audio.speaker.stream?.is_muted || isUnwantedSinkSelected.value ? 0 : [99, 66, 33, 1, 0].find(threshold => threshold <= Audio.speaker.volume * 100)
                self.icon = `audio-volume-${category[icon]}-symbolic`
            }),
            Revealer({
                reveal_child: speakerRevealerState.bind(),
                child: Label({className: "revealerLabel"}).hook(Audio.speaker, self => {
                    self.label = isUnwantedSinkSelected.value ? 'N/A' : `%${Math.round(Audio.speaker.volume * 100)}`
                }),
                transition: 'slide_left',
            }),
        ]
    })
})
.on("enter-notify-event", () => speakerRevealerState.value = true)
.on("leave-notify-event", () => speakerRevealerState.value = false)


const microphoneVolume = () => Button({
    on_scroll_up: () => Audio.microphone.volume < 0.9 ? Audio.microphone.volume += 0.1 : Audio.microphone.volume = 1,
    on_scroll_down: () => Audio.microphone.volume -= 0.1,
    onClicked: () => Utils.execAsync(['pactl', 'set-source-mute', '@DEFAULT_SOURCE@', 'toggle']),
	child: Box({
        children: [
            Icon({className: 'revealerIcon'}).hook(Audio.microphone, self => {
                const icon = Audio.microphone.stream?.is_muted ? 0 : [66, 33, 1, 0].find(threshold => threshold <= Audio.microphone.volume * 100)
                self.icon = `microphone-sensitivity-${category[icon]}-symbolic`
            }),
            Revealer({
                reveal_child: microphoneRevealerState.bind(),
                child: Label({className: "revealerLabel"}).hook(Audio.microphone, self => {
                    self.label = Audio.microphone.description == null ? 'N/A' : `%${Math.round(Audio.microphone.volume * 100)}`
                }),
                transition: 'slide_left',
            }),
        ]
    })
})
.on("enter-notify-event", () => microphoneRevealerState.value = true)
.on("leave-notify-event", () => microphoneRevealerState.value = false)



const Left = () => Box({
    spacing: 8,
    children: [
        //Workspaces(),
        staticWorkspaces(),
    ],
})

const Center = () => Box({
    spacing: 8,
    children: [
        Clock()
    ],
})

const Right = () => Box({
    hpack: 'end',
    //spacing: 8,
    children: [
        cache(),
        microphoneVolume(),
        speakerVolume(),
        audioOutputSwitch(),
    ],
})

const Bar = (monitor = 0) => Window({
    name: `bar-${monitor}`, // name has to be unique
    className: 'bar',
    monitor,
    anchor: ['top', 'left', 'right'],
    exclusivity: 'exclusive',
    child: CenterBox({
        start_widget: CenterBox({
            start_widget: Left(),
            center_widget: CenterBox({
                start_widget: temps(),
                end_widget: percentages()
            })
        }),
        center_widget: Center(),
        end_widget: CenterBox({
            center_widget: nowPlaying(),
            end_widget: Right()
        }),
    }),
})

App.config({
    style: './style.css',
    windows: [Bar()]
})
