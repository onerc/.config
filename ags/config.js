const Hyprland = await Service.import('hyprland')
const Mpris = await Service.import('mpris')
const Audio = await Service.import('audio')
const { Button, Box, CenterBox, Icon, Label, Revealer, Window } = Widget

const speakerRevealerState = Variable(false)
const microphoneRevealerState = Variable(false)
const cacheRevealerState = Variable(false)
const isUnwantedSinkSelected = Variable(false)
const unwantedSink = 'iec958'

const category = {
    99: 'overamplified',
    66: 'high',
    33: 'medium',
    1: 'low',
    0: 'muted'
}

const audioOutputSwitch = () => Button({
    on_clicked: () => Audio.speaker = Audio.speakers.find(sink => {return sink.stream !== Audio.speaker.stream}),
    on_middle_click: () => console.log(Mpris),
    child: Icon().hook(Audio.speaker, self => {
        if (Audio.speaker.name?.includes('hdmi')) {
            self.icon = "video-display-symbolic"
            self.size = 12
        } else if (Audio.speaker.name?.includes('analog')) {
            self.icon = "audio-headphones-symbolic"
            self.size = 14
        } 
        // else
        //     self.label = ""
    }),
})

const staticWorkspaces = () => Box({
    children: [1,2,3,4,5,6,7,8,9,10].map(numb=>Button({
        on_clicked: () => Hyprland.messageAsync(`dispatch workspace ${numb}`),
        child: Label(`${numb}`),
    }))
})

const Workspaces = () => Box({
    children: Hyprland.bind('workspaces').transform(ws => {
        return ws.sort((a, b) => a.id - b.id).map(({ id }) => Button({
            on_clicked: () => Hyprland.messageAsync(`dispatch workspace ${id}`),
            child: Label(`${id}`),
            //class_name: Hyprland.active.workspace.bind('id').transform(i => `${i === id ? 'focused' : ''}`),
        }))
    }),
})

const Clock = () => Label({
    setup: self => self.poll(1000, self => Utils.execAsync(['date', '+%H:%M']).then(date => self.label = date)),
})

const cache = () => Button({
    child: Box({
        children: [
            Icon({css: 'padding-left: 4px', icon: 'drive-removable-media-symbolic'}),
            Revealer({
                reveal_child: cacheRevealerState.bind(),
                child: Label({css:'min-width: 2.6rem; padding: 0px 4px',
                    setup: self => self.poll(1000, self => Utils.execAsync(['bash', '-c', "grep Dirty: /proc/meminfo | awk '{print $2$3}'"]).then(cacheinfo => self.label = cacheinfo))
                }),
                transition: 'slide_left',
            })
        ]
    })
})
.on("enter-notify-event", () => cacheRevealerState.value = true)
.on("leave-notify-event", () => cacheRevealerState.value = false)

const nowPlaying = () => Button({
    on_clicked: () => Mpris.getPlayer()?.playPause(),
    on_scroll_up: () => Mpris.getPlayer()?.next(),
    on_scroll_down: () => Mpris.getPlayer()?.previous(),
    on_middle_click: () => Mpris.getPlayer()?.stop(),
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
    on_scroll_up: () => {if (!(isUnwantedSinkSelected.value)) {Audio.speaker.volume < 0.9 ? Audio.speaker.volume += 0.1 : Audio.speaker.volume = 1}},
    on_scroll_down: () => {if (!(isUnwantedSinkSelected.value)) {Audio.speaker.volume -= 0.1}},
    on_clicked: () => Utils.execAsync(['pactl', 'set-sink-mute', '@DEFAULT_SINK@', 'toggle']),
	child: Box({
        children: [
            Icon({css:'padding-left: 4px'}).hook(Audio.speaker, self => {
                isUnwantedSinkSelected.value = Audio.speaker.name?.includes(unwantedSink)
                const icon = Audio.speaker.stream?.is_muted || isUnwantedSinkSelected.value ? 0 : [99, 66, 33, 1, 0].find(threshold => threshold <= Audio.speaker.volume * 100)
                self.icon = `audio-volume-${category[icon]}-symbolic`
            }),
            Revealer({
                reveal_child: speakerRevealerState.bind(),
                child: Label({css: 'min-width: 2.6rem; padding: 0px 4px'}).hook(Audio.speaker, self => {
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
    on_clicked: () => Utils.execAsync(['pactl', 'set-source-mute', '@DEFAULT_SOURCE@', 'toggle']),
	child: Box({
        children: [
            Icon({css:'padding-left: 4px'}).hook(Audio.microphone, self => {
                const icon = Audio.microphone.stream?.is_muted ? 0 : [66, 33, 1, 0].find(threshold => threshold <= Audio.microphone.volume * 100)
                self.icon = `microphone-sensitivity-${category[icon]}-symbolic`
            }),
            Revealer({
                reveal_child: microphoneRevealerState.bind(),
                child: Label({css: 'min-width: 2.6rem; padding: 0px 4px'}).hook(Audio.microphone, self => {
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
        Clock(),
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
    class_name: 'bar',
    monitor,
    anchor: ['top', 'left', 'right'],
    exclusivity: 'exclusive',
    child: CenterBox({
        start_widget: Left(),
        center_widget: Center(),
        end_widget: CenterBox({
            center_widget: nowPlaying(),
            end_widget: Right()
        }),
    }),
})

App.config({
    windows: [Bar()]
})
