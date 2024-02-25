const Hyprland = await Service.import('hyprland')
const Mpris = await Service.import('mpris')
const Audio = await Service.import('audio')

const outputSwitch = () => Widget.Button({
    on_clicked: () => Audio.speaker = Audio.speakers.find(sink => {return sink.stream !== Audio.speaker.stream}),
    on_middle_click: () => console.log(),
    child: Widget.Label('???').hook(Audio.speaker, self => {
        if (Audio.speaker.description?.includes('HDMI')) {
            self.label = ""
        } else {
            self.label = ""
        }
    }),
});

const staticWorkspaces = () => Widget.Box({
    children: [1,2,3,4,5,6,7,8,9,10].map(numb=>Widget.Button({
    on_clicked: () => Hyprland.messageAsync(`dispatch workspace ${numb}`),
    child: Widget.Label(`${numb}`),
    }))
})

const Workspaces = () => Widget.Box({
    children: Hyprland.bind('workspaces').transform(ws => {
        return ws.sort((a, b) => a.id - b.id).map(({ id }) => Widget.Button({
            on_clicked: () => Hyprland.messageAsync(`dispatch workspace ${id}`),
            child: Widget.Label(`${id}`),
            //class_name: Hyprland.active.workspace.bind('id').transform(i => `${i === id ? 'focused' : ''}`),
        }));
    }),
});

const Clock = () => Widget.Label({
    setup: self => self.poll(1000, self => Utils.execAsync(['date', '+%H:%M:%S']).then(date => self.label = date)),
});

const nowPlaying = () => Widget.Button({
    on_clicked: () => Mpris.getPlayer('')?.playPause(),
    on_scroll_up: () => Mpris.getPlayer('')?.next(),
    on_scroll_down: () => Mpris.getPlayer('')?.previous(),
    child: Widget.Label('-').hook(Mpris, self => {
        if (Mpris.players[0]) {
            const { track_artists, track_title } = Mpris.players[0];
            self.label = `${track_artists.join(', ')} - ${track_title}`;
        } else {
            self.label = 'Nothing is playing';
        }
    }, 'player-changed'),
});

const speakerVolume = () => Widget.Button({
    on_clicked: () =>  Utils.execAsync(['pactl', 'set-sink-mute', '@DEFAULT_SINK@', 'toggle']), // Audio.speaker.is_muted = !Audio.speaker.is_muted makes volume zero and mutes??
	on_scroll_up: () => Utils.execAsync(['.config/eww/scripts/superdupervolumecontrol.sh','sink', 'up']),
	on_scroll_down: () => Utils.execAsync(['.config/eww/scripts/superdupervolumecontrol.sh','sink', 'down']),
	child: Widget.Box({
        children: [
            Widget.Icon().hook(Audio.speaker, self => {
                const category = {
                    100: 'overamplified',
                    66: 'high',
                    33: 'medium',
                    1: 'low',
                    0: 'muted',
                };
                const icon = Audio.speaker.stream?.is_muted ? 0 : [100, 66, 33, 1, 0].find(threshold => threshold <= Audio.speaker.volume * 100);
                self.icon = `audio-volume-${category[icon]}-symbolic`;}),
                Widget.Label('bad speaker').hook(Audio, self => {self.label = ` %${Math.round(Audio.speaker.volume*100)}`}),           
        ],
    }),
});

const microphoneVolume = () => Widget.Button({
    on_clicked: () => Utils.execAsync(['pactl', 'set-source-mute', '@DEFAULT_SOURCE@', 'toggle']),
    on_scroll_up: () => Utils.execAsync(['.config/eww/scripts/superdupervolumecontrol.sh','source', 'up']),
    on_scroll_down: () => Utils.execAsync(['.config/eww/scripts/superdupervolumecontrol.sh','source', 'down']),
    child: Widget.Box({
        children: [
            Widget.Icon().hook(Audio.microphone, self => {
                const category = {
                    67: 'high',
                    34: 'medium',
                    1: 'low',
                    0: 'muted',
                };
                const icon = Audio.microphone.stream?.is_muted ? 0 : [67, 34, 1, 0].find(threshold => threshold <= Audio.microphone.volume * 100);
                self.icon = `microphone-sensitivity-${category[icon]}-symbolic`;}),
                Widget.Label('bad mic').hook(Audio, self => {self.label = ` %${Math.round(Audio.microphone.volume*100)}`}),
        ],
    }),
});

const Left = () => Widget.Box({
    spacing: 8,
    children: [
        //Workspaces(),
        staticWorkspaces(),
    ],
});

const Center = () => Widget.Box({
    spacing: 8,
    children: [
        Clock(),
    ],
});

const Right = () => Widget.Box({
    hpack: 'end',
    //spacing: 8,
    children: [
        nowPlaying(),
        microphoneVolume(),
        speakerVolume(),
        outputSwitch(),
    ],
});

const Bar = (monitor = 0) => Widget.Window({
    name: `bar-${monitor}`, // name has to be unique
    class_name: 'bar',
    monitor,
    anchor: ['top', 'left', 'right'],
    exclusivity: 'exclusive',
    child: Widget.CenterBox({
        start_widget: Left(),
        center_widget: Center(),
        end_widget: Right(),
    }),
});

export default {
    windows: [
        Bar()
    ],
};
