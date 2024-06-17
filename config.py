def config():
    return {
        "rev": [
            1,
            0
        ],
        "vid": 2210301,
        "id": {
            "mdns": "wled-slwf03",
            "name": "Smlight SLWF-03",
            "inv": "Light"
        },
        "nw": {
            "ins": [
                {
                    "ssid": "KCC",
                    "pskl": 12,
                    "ip": [
                        0,
                        0,
                        0,
                        0
                    ],
                    "gw": [
                        0,
                        0,
                        0,
                        0
                    ],
                    "sn": [
                        255,
                        255,
                        255,
                        0
                    ]
                }
            ]
        },
        "ap": {
            "ssid": "WLED-AP",
            "pskl": 8,
            "chan": 1,
            "hide": 0,
            "behav": 0,
            "ip": [
                4,
                3,
                2,
                1
            ]
        },
        "wifi": {
            "sleep": false
        },
        "hw": {
            "led": {
                "total": 1303,
                "maxpwr": 10000,
                "ledma": 255,
                "cct": false,
                "cr": false,
                "cb": 0,
                "fps": 42,
                "rgbwm": 3,
                "somp": 0,
                "mxw": 1303,
                "mxh": 1,
                "mxp": 0,
                "mph": 1,
                "mpv": 1,
                "pfltb": 0,
                "pfllr": 0,
                "pohv": 0,
                "pnls": 0,
                "pnlt": 0,
                "ins": [
                    {
                        "start": 0,
                        "len": 616,
                        "pin": [
                            16
                        ],
                        "order": 0,
                        "rev": true,
                        "skip": 0,
                        "type": 22,
                        "ref": false
                    },
                    {
                        "start": 616,
                        "len": 687,
                        "pin": [
                            17
                        ],
                        "order": 0,
                        "rev": false,
                        "skip": 0,
                        "type": 22,
                        "ref": false
                    }
                ]
            },
            "com": [],
            "btn": {
                "max": 4,
                "ins": [
                    {
                        "type": 3,
                        "pin": [
                            26
                        ],
                        "macros": [
                            0,
                            0,
                            0
                        ]
                    },
                    {
                        "type": 0,
                        "pin": [
                            -1
                        ],
                        "macros": [
                            0,
                            0,
                            0
                        ]
                    },
                    {
                        "type": 0,
                        "pin": [
                            -1
                        ],
                        "macros": [
                            0,
                            0,
                            0
                        ]
                    },
                    {
                        "type": 0,
                        "pin": [
                            -1
                        ],
                        "macros": [
                            0,
                            0,
                            0
                        ]
                    }
                ],
                "tt": 32,
                "mqtt": false
            },
            "ir": {
                "pin": 4,
                "type": 8,
                "sel": true
            },
            "relay": {
                "pin": -1,
                "rev": false
            },
            "baud": 1152,
            "analogmic": {
                "pin": 36
            },
            "digitalmic": {
                "en": 1,
                "pins": {
                    "i2ssd": 32,
                    "i2sws": 15,
                    "i2sck": 14
                }
            }
        },
        "light": {
            "scale-bri": 100,
            "pal-mode": 0,
            "aseg": false,
            "gc": {
                "bri": 1,
                "col": 2.8
            },
            "tr": {
                "mode": true,
                "dur": 7,
                "pal": 0
            },
            "nl": {
                "mode": 1,
                "dur": 60,
                "tbri": 0,
                "macro": 0
            }
        },
        "def": {
            "ps": 2,
            "on": true,
            "bri": 128
        },
        "if": {
            "sync": {
                "port0": 21324,
                "port1": 65506,
                "recv": {
                    "bri": true,
                    "col": true,
                    "fx": true,
                    "grp": 1,
                    "seg": false,
                    "sb": false
                },
                "send": {
                    "dir": false,
                    "btn": false,
                    "va": false,
                    "hue": false,
                    "macro": false,
                    "twice": false,
                    "grp": 1
                }
            },
            "nodes": {
                "list": false,
                "bcast": false
            },
            "live": {
                "en": true,
                "mso": false,
                "port": 5568,
                "mc": false,
                "dmx": {
                    "uni": 1,
                    "seqskip": false,
                    "addr": 1,
                    "mode": 4
                },
                "timeout": 25,
                "maxbri": false,
                "no-gc": true,
                "offset": 0
            },
            "va": {
                "alexa": false,
                "macros": [
                    0,
                    0
                ]
            },
            "mqtt": {
                "en": false,
                "broker": "",
                "port": 1883,
                "user": "",
                "pskl": 0,
                "cid": "WLED-52226c",
                "topics": {
                    "device": "wled/52226c",
                    "group": "wled/all"
                }
            },
            "hue": {
                "en": false,
                "id": 1,
                "iv": 25,
                "recv": {
                    "on": true,
                    "bri": true,
                    "col": true
                },
                "ip": [
                    192,
                    168,
                    4,
                    0
                ]
            },
            "ntp": {
                "en": false,
                "host": "0.wled.pool.ntp.org",
                "tz": 0,
                "offset": 0,
                "ampm": false,
                "ln": 0,
                "lt": 0
            }
        },
        "ol": {
            "clock": 0,
            "cntdwn": false,
            "min": 0,
            "max": 29,
            "o12pix": 0,
            "o5m": false,
            "osec": false
        },
        "timers": {
            "cntdwn": {
                "goal": [
                    20,
                    1,
                    1,
                    0,
                    0,
                    0
                ],
                "macro": 0
            },
            "ins": []
        },
        "ota": {
            "lock": false,
            "lock-wifi": false,
            "pskl": 7,
            "aota": false
        },
        "snd": {
            "cfg": {
                "sq": 10,
                "gn": 30,
                "agc": 0
            },
            "custom": {
                "c1": 128,
                "c2": 128,
                "c3": 128
            },
            "sync": {
                "port": 11988,
                "en": 0
            }
        },
        "um": {
            "Autosave": {
                "enabled": true,
                "autoSaveAfterSec": 15,
                "autoSavePreset": 250,
                "autoSaveApplyOnBoot": true
            }
        }
    }