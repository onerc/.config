const Hyprland = await Service.import('hyprland')
const Mpris = await Service.import('mpris')
const Audio = await Service.import('audio')
const { Button, Box, CenterBox, Icon, Label, Revealer, Stack, Window } = Widget

const speakerRevealerState = Variable(false)
const microphoneRevealerState = Variable(false)

const cacheRevealerState = Variable(false)
const cacheButtonPin = Variable(false)

const tempsRevealerState = Variable(false)
const tempsButtonPin = Variable(false)

const percentagesRevealerState = Variable(false)
const percentagesButtonPin = Variable(false)

const powerRevealerState = Variable(false)

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
    poll: [1000, ['bash', '-c', "top -bn 1 | awk '/Cpu/{print 100-$8}'"], value => `${Math.round(value)}%`]
})

const ram = Variable('', {
    poll: [1000, ['bash', '-c', "free | awk '/Mem/{print $3/$2 * 100}'"], value => `${Math.round(value)}%`]
})

const cachePoll = Variable('', {
    poll: [1000, ['bash', '-c', "grep Dirty: /proc/meminfo | awk '{print $2}'"], value => {
        if (value >= 1048576) {
            return `${(value / 1048576).toFixed(1)} GB`
        } else if (value >= 1024) {
            return `${(value / 1024).toFixed(1)} MB`
        } else {
            return `${value} KB`
        }
    }]
})

const audioOutputSwitch = () => Button({
    onClicked: () => Audio.speaker = Audio.speakers.find(sink => { return sink.stream !== Audio.speaker.stream }),
    onMiddleClick: () => console.log(Mpris.players[0]),
    child: Icon().hook(Audio.speaker, self => {
        if (Audio.speaker.name?.includes('hdmi')) {
            self.icon = 'video-display-symbolic'
            self.size = 12
        } else if (Audio.speaker.name?.includes('analog')) {
            self.icon = 'audio-headphones-symbolic'
            self.size = 14
        } else {
            self.icon = 'dialog-error-symbolic'
        }
    }),
})

const staticWorkspaces = () => Box({
    children: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(numb => Button({
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
    onClicked: () => cacheButtonPin.value = !cacheButtonPin.value,
    child: Box({
        children: [
            Icon({
                className: 'revealerIcon',
                icon: cacheButtonPin.bind().as(value => value ? 'lock-symbolic' : 'drive-removable-media-symbolic')
            }),
            Revealer({
                reveal_child: cacheRevealerState.bind(),
                child: Label({
                    className: 'revealerLabel',
                    label: cachePoll.bind()
                }),
                transition: 'slide_left',
            })
        ]
    })
})
    .on('enter-notify-event', () => cacheRevealerState.value = true)
    .on('leave-notify-event', () => { if (!cacheButtonPin.value) { cacheRevealerState.value = false } })


const temps = () => Button({
    onClicked: () => tempsButtonPin.value = !tempsButtonPin.value,
    child: Box({
        children: [
            Revealer({
                reveal_child: tempsRevealerState.bind(),
                child: Box({
                    children: [
                        Icon({
                            className: 'revealerIcon',
                            icon: 'cpu-symbolic'
                        }),
                        Label({
                            className: 'revealerLabel',
                            label: sensors.bind().as(value => `${value['coretemp-isa-0000']['Package id 0']['temp1_input']} °C`)
                        })
                    ]
                }),
                transition: 'slide_left',
            }),
            Icon({
                className: 'revealerIcon',
                icon: tempsButtonPin.bind().as(value => value ? 'lock-symbolic' : 'temp-symbolic')
            }),
            Revealer({
                reveal_child: tempsRevealerState.bind(),
                child: Box({
                    children: [
                        Label({
                            className: 'revealerLabel',
                            label: sensors.bind().as(value => `${value['amdgpu-pci-0300']['junction']['temp2_input']} °C`)
                        }),
                        Icon({
                            className: 'revealerIcon',
                            icon: 'freon-gpu-temperature-symbolic'
                        })
                    ]
                }),
                transition: 'slide_right',
            }),

        ]
    })
})
    .on('enter-notify-event', () => tempsRevealerState.value = true)
    .on('leave-notify-event', () => { if (!tempsButtonPin.value) { tempsRevealerState.value = false } })

const percentages = () => Button({
    onClicked: () => percentagesButtonPin.value = !percentagesButtonPin.value,
    child: Box({
        children: [
            Revealer({
                reveal_child: percentagesRevealerState.bind(),
                child: Box({
                    children: [
                        Icon({
                            className: 'revealerIcon',
                            icon: 'cpu-symbolic'
                        }),
                        Label({
                            className: 'revealerLabel',
                            label: cpu.bind()
                        })
                    ]
                }),
                transition: 'slide_left',
            }),
            Icon({
                className: 'revealerIcon',
                icon: percentagesButtonPin.bind().as(value => value ? 'lock-symbolic' : 'edit-find-symbolic')
            }),
            Revealer({
                reveal_child: percentagesRevealerState.bind(),
                child: Box({
                    children: [
                        Label({
                            className: 'revealerLabel',
                            label: ram.bind()
                        }),
                        Icon({
                            className: 'revealerIcon',
                            icon: 'ram-symbolic'
                        })
                    ]
                }),
                transition: 'slide_right',
            }),

        ]
    })
})
    .on('enter-notify-event', () => percentagesRevealerState.value = true)
    .on('leave-notify-event', () => { if (!percentagesButtonPin.value) { percentagesRevealerState.value = false } })



const nowPlaying = () => Button({
    onClicked: () => Mpris.getPlayer()?.playPause(),
    onScrollUp: () => Mpris.getPlayer()?.next(),
    onScrollDown: () => Mpris.getPlayer()?.previous(),
    onMiddleClick: () => Mpris.getPlayer()?.stop(),
    child: Label('-').hook(Mpris, self => {
        if (Mpris.players[0]) {
            const { track_artists, track_title, track_album } = Mpris.players[0]
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
    onScrollUp: () => { if (!isUnwantedSinkSelected.value) { Audio.speaker.volume < 0.9 ? Audio.speaker.volume += 0.1 : Audio.speaker.volume = 1 } },
    onScrollDown: () => { if (!isUnwantedSinkSelected.value) { Audio.speaker.volume -= 0.1 } },
    onClicked: () => Audio.speaker.is_muted = !Audio.speaker.is_muted,
    child: Box({
        children: [
            Stack({
                transition: 'slide_up_down',
                children: (() => {
                    const levels = ['overamplified', 'high', 'medium', 'low', 'muted']
                    const icons = {}
                    levels.forEach(level => {
                        icons[level] = Icon({ icon: `audio-volume-${level}-symbolic`, className: 'revealerIcon' })
                    })
                    return icons
                })(),
            }).hook(Audio.speaker, self => {
                const icon = Audio.speaker.stream?.is_muted ? 0 : [99, 66, 33, 1, 0].find(threshold => threshold <= Audio.speaker.volume * 100)
                self.shown = `${category[icon]}`
            }),
            Revealer({
                reveal_child: speakerRevealerState.bind(),
                child: Stack({
                    transition: 'slide_up_down',
                    children: (() => {
                        const percentages = {}
                        for (let i = 100; i >= 0; i -= 10) {
                            percentages[`%${i}`] = Label({ label: `%${i}`, className: 'revealerLabel' })
                        }
                        return percentages
                    })(),
                }).hook(Audio.speaker, self => { self.shown = `%${Math.round(Audio.speaker.volume * 100)}` }),
                transition: 'slide_left',
            }),
        ]
    })
})
    .on('enter-notify-event', () => speakerRevealerState.value = true)
    .on('leave-notify-event', () => speakerRevealerState.value = false)


const microphoneVolume = () => Button({
    onScrollUp: () => Audio.microphone.volume < 0.9 ? Audio.microphone.volume += 0.1 : Audio.microphone.volume = 1,
    onScrollDown: () => Audio.microphone.volume -= 0.1,
    onClicked: () => Audio.microphone.is_muted = !Audio.microphone.is_muted,
    child: Box({
        children: [
            Stack({
                transition: 'slide_up_down',
                children: (() => {
                    const levels = ['high', 'medium', 'low', 'muted']
                    const icons = {}
                    levels.forEach(level => {
                        icons[level] = Icon({ icon: `microphone-sensitivity-${level}-symbolic`, className: 'revealerIcon' })
                    })
                    return icons
                })(),
            }).hook(Audio.microphone, self => {
                const icon = Audio.microphone.stream?.is_muted ? 0 : [66, 33, 1, 0].find(threshold => threshold <= Audio.microphone.volume * 100)
                self.shown = `${category[icon]}`
            }),
            Revealer({
                reveal_child: microphoneRevealerState.bind(),
                child: Stack({
                    transition: 'slide_up_down',
                    children: (() => {
                        const percentages = {}
                        for (let i = 100; i >= 0; i -= 10) {
                            percentages[`%${i}`] = Label({ label: `%${i}`, className: 'revealerLabel' })
                        }
                        return percentages
                    })(),
                }).hook(Audio.microphone, self => {self.shown = `%${Math.round(Audio.microphone.volume * 100)}`}),
                transition: 'slide_left',
            }),
        ]
    })
})
    .on('enter-notify-event', () => microphoneRevealerState.value = true)
    .on('leave-notify-event', () => microphoneRevealerState.value = false)

const currentLabel = Variable("locked")
const currentIcon = Variable("shutdown")
const transitionAnim = Variable('slide_left_right')

const setTransitionAndLabel = (transition, label) => {
    transitionAnim.value = transition
    currentLabel.value = label
}
const power = () => Button({
    onClicked: () => {
        switch (currentLabel.value) {
            case "shutdown":
                Utils.execAsync("shutdown now")
                // console.log("shutdown")
                break
            case "reboot":
                Utils.execAsync("reboot")
                // console.log("reboot")
                break
        }
    },

    onSecondaryClick: () => {
        setTransitionAndLabel('slide_left_right', currentIcon.value)
    },

    onSecondaryClickRelease: () => {
        setTransitionAndLabel('slide_left_right', 'locked')
    },

    onScrollUp: () => {
        setTransitionAndLabel('slide_up_down', currentLabel.value != "locked" ? "shutdown" : currentLabel.value)
        currentIcon.value = "shutdown"
    },

    onScrollDown: () => {
        setTransitionAndLabel('slide_up_down', currentLabel.value != "locked" ? "reboot" : currentLabel.value)
        currentIcon.value = "reboot"
    },


    child: Box({
        children: [
            Stack({
                transition: 'slide_up_down',
                children: {
                    'shutdown': Icon({ icon: 'system-shutdown-symbolic' }),
                    'reboot': Icon({ icon: 'system-reboot-symbolic' })
                },
                shown: currentIcon.bind()
            }),
            Revealer({
                child: Stack({
                    transition: transitionAnim.bind(),
                    children: {
                        'locked': Label({ label: 'Locked' }),
                        'shutdown': Label({ label: 'Shutdown' }),
                        'reboot': Label({ label: 'Reboot' }),
                    },
                    shown: currentLabel.bind()
                }),
                transition: "slide_left",
                reveal_child: powerRevealerState.bind()
            })

        ]
    })
})
    .on('enter-notify-event', () => powerRevealerState.value = true)
    .on('leave-notify-event', () => powerRevealerState.value = false)


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
        percentages(),
        Clock(),
        temps()
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
        power(),
    ],
})

const Bar = (monitor = 0) => Window({
    name: `bar-${monitor}`, // name has to be unique
    className: 'bar',
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
    style: './style.css',
    windows: [Bar()]
})
