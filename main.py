import json
import time
import random
from base64 import b64decode, b64encode
from execjs import compile
from requests import Session
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

with open("api.js") as file:
    ctx = compile(file.read())

def format_value(value):
    if isinstance(value, list):
        if not value:
            return ""
        return ",".join(format_value(v) for v in value)
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)

def format_fe(t):
    if not t or not isinstance(t, dict):
        return []
    return [format_value(t[n]) for n in t]

class Arkose:
    def __init__(self) -> None:
        self.session = Session()

        timestamp = time.time()
        self.timestamp = round(timestamp)
        self.ark_esync_value = round(timestamp - (timestamp % 21600))

    def call_d(self, text: str, iter: int = 0):
        return ctx.call("d", text, iter)

    def call_ie(self, text, encoded: bool = False):
        return ctx.call("IE", text, encoded)

    def get_fingerprint(self):
        f = {
            "DNT": "unknown",
            "L": "fr-FR",
            "D": 24,
            "PR": 1,
            "S": [1920, 1080],
            "AS": [1920, 1032],
            "TO": -120,
            "SS": True,
            "LS": True,
            "IDB": True,
            "B": False,
            "ODB": False,
            "CPUC": "unknown",
            "PK": "Win32",
            "CFP": 296271673,
            "FR": False,
            "FOS": False,
            "FB": False,
            "JSF": [],
            "P": [
                "Chrome PDF Viewer",
                "Chromium PDF Viewer",
                "Microsoft Edge PDF Viewer",
                "PDF Viewer",
                "WebKit built-in PDF",
            ],
            "T": [0, False, False],
            "H": 12,
            "SWF": False,
        }
        fe = [f"{k}:{v}" for k, v in f.items()]
        fe2 = ";".join(str(x) for x in format_fe(f))

        wh2 = [
            "TEMPORARY",
            "PERSISTENT",
            "constructor",
            "addEventListener",
            "dispatchEvent",
            "removeEventListener",
            "constructor",
            "when",
            "constructor",
            "__defineGetter__",
            "__defineSetter__",
            "hasOwnProperty",
            "__lookupGetter__",
            "__lookupSetter__",
            "isPrototypeOf",
            "propertyIsEnumerable",
            "toString",
            "valueOf",
            "__proto__",
            "toLocaleString",
        ]

        return [
            {"key": "api_type", "value": "js"},
            {"key": "f", "value": self.call_d(fe2)},
            {"key": "n", "value": b64encode(str(self.timestamp).encode()).decode()},
            {
                "key": "wh",
                "value": f"ae88f94933ccdf0a2f586757f885f221|{self.call_d('|'.join(wh2), 420)}",
            },
            {
                "key": "enhanced_fp",
                "value": [
                    {
                        "key": "webgl_extensions",
                        "value": "ANGLE_instanced_arrays;EXT_blend_minmax;EXT_clip_control;EXT_color_buffer_half_float;EXT_depth_clamp;EXT_disjoint_timer_query;EXT_float_blend;EXT_frag_depth;EXT_polygon_offset_clamp;EXT_shader_texture_lod;EXT_texture_compression_bptc;EXT_texture_compression_rgtc;EXT_texture_filter_anisotropic;EXT_texture_mirror_clamp_to_edge;EXT_sRGB;KHR_parallel_shader_compile;OES_element_index_uint;OES_fbo_render_mipmap;OES_standard_derivatives;OES_texture_float;OES_texture_float_linear;OES_texture_half_float;OES_texture_half_float_linear;OES_vertex_array_object;WEBGL_blend_func_extended;WEBGL_color_buffer_float;WEBGL_compressed_texture_s3tc;WEBGL_compressed_texture_s3tc_srgb;WEBGL_debug_renderer_info;WEBGL_debug_shaders;WEBGL_depth_texture;WEBGL_draw_buffers;WEBGL_lose_context;WEBGL_multi_draw;WEBGL_polygon_mode",
                    },
                    {
                        "key": "webgl_extensions_hash",
                        "value": "7300c23f4e6fa34e534fc99c1b628588",
                    },
                    {"key": "webgl_renderer", "value": "WebKit WebGL"},
                    {"key": "webgl_vendor", "value": "WebKit"},
                    {
                        "key": "webgl_version",
                        "value": "WebGL 1.0 (OpenGL ES 2.0 Chromium)",
                    },
                    {
                        "key": "webgl_shading_language_version",
                        "value": "WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)",
                    },
                    {"key": "webgl_aliased_line_width_range", "value": "[1, 1]"},
                    {"key": "webgl_aliased_point_size_range", "value": "[1, 1024]"},
                    {"key": "webgl_antialiasing", "value": "yes"},
                    {"key": "webgl_bits", "value": "8,8,24,8,8,0"},
                    {
                        "key": "webgl_max_params",
                        "value": "16,32,16384,1024,16384,16,16384,30,16,16,4096",
                    },
                    {"key": "webgl_max_viewport_dims", "value": "[32767, 32767]"},
                    {"key": "webgl_unmasked_vendor", "value": "Google Inc. (AMD)"},
                    {
                        "key": "webgl_unmasked_renderer",
                        "value": "ANGLE (AMD, AMD Radeon RX 6650 XT (0x000073EF) Direct3D11 vs_5_0 ps_5_0, D3D11)",
                    },
                    {
                        "key": "webgl_vsf_params",
                        "value": "23,127,127,23,127,127,23,127,127",
                    },
                    {"key": "webgl_vsi_params", "value": "0,31,30,0,31,30,0,31,30"},
                    {
                        "key": "webgl_fsf_params",
                        "value": "23,127,127,23,127,127,23,127,127",
                    },
                    {"key": "webgl_fsi_params", "value": "0,31,30,0,31,30,0,31,30"},
                    {
                        "key": "webgl_hash_webgl",
                        "value": "27e6fa49ecedd71019e081ef99a3eac9",
                    },
                    {
                        "key": "user_agent_data_brands",
                        "value": "Not)A;Brand,Chromium,Google Chrome",
                    },
                    {"key": "user_agent_data_mobile", "value": False},
                    {"key": "navigator_connection_downlink", "value": 1.45},
                    {"key": "navigator_connection_downlink_max", "value": None},
                    {"key": "network_info_rtt", "value": 300},
                    {"key": "network_info_save_data", "value": False},
                    {"key": "network_info_rtt_type", "value": None},
                    {"key": "screen_pixel_depth", "value": 24},
                    {"key": "navigator_device_memory", "value": 8},
                    {"key": "navigator_pdf_viewer_enabled", "value": True},
                    {"key": "navigator_languages", "value": "fr-FR,fr,en-US,en"},
                    {"key": "window_inner_width", "value": 0},
                    {"key": "window_inner_height", "value": 0},
                    {"key": "window_outer_width", "value": 974},
                    {"key": "window_outer_height", "value": 1039},
                    {"key": "browser_detection_firefox", "value": False},
                    {"key": "browser_detection_brave", "value": False},
                    {
                        "key": "browser_api_checks",
                        "value": [
                            "permission_status: True",
                            "eye_dropper: True",
                            "audio_data: True",
                            "writable_stream: True",
                            "css_style_rule: True",
                            "navigator_ua: True",
                            "barcode_detector: False",
                            "display_names: True",
                            "contacts_manager: False",
                            "svg_discard_element: False",
                            "usb: defined",
                            "media_device: defined",
                            "playback_quality: True",
                        ],
                    },
                    {
                        "key": "browser_object_checks",
                        "value": "554838a8451ac36cb977e719e9d6623c",
                    },
                    {"key": "29s83ih9", "value": f"{Arkose().call_ie(False)}⁣"},
                    {
                        "key": "audio_codecs",
                        "value": '{"ogg":"probably","mp3":"probably","wav":"probably","m4a":"maybe","aac":"probably"}',
                    },
                    {
                        "key": "audio_codecs_extended_hash",
                        "value": Arkose().call_ie('{"audio/mp4; codecs=\\"mp4a.40\\"":{"canPlay":"maybe","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.1\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.2\\"":{"canPlay":"probably","mediaSource":true},"audio/mp4; codecs=\\"mp4a.40.3\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.4\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.5\\"":{"canPlay":"probably","mediaSource":true},"audio/mp4; codecs=\\"mp4a.40.6\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.7\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.8\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.9\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.12\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.13\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.14\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.15\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.16\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.17\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.19\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.20\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.21\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.22\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.23\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.24\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.25\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.26\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.27\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.28\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.29\\"":{"canPlay":"probably","mediaSource":true},"audio/mp4; codecs=\\"mp4a.40.32\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.33\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.34\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.35\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.40.36\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"mp4a.66\\"":{"canPlay":"probably","mediaSource":false},"audio/mp4; codecs=\\"mp4a.67\\"":{"canPlay":"probably","mediaSource":true},"audio/mp4; codecs=\\"mp4a.68\\"":{"canPlay":"probably","mediaSource":false},"audio/mp4; codecs=\\"mp4a.69\\"":{"canPlay":"probably","mediaSource":false},"audio/mp4; codecs=\\"mp4a.6B\\"":{"canPlay":"probably","mediaSource":false},"audio/mp4; codecs=\\"mp3\\"":{"canPlay":"probably","mediaSource":false},"audio/mp4; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":true},"audio/mp4; codecs=\\"bogus\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"aac\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"ac3\\"":{"canPlay":"","mediaSource":false},"audio/mp4; codecs=\\"A52\\"":{"canPlay":"","mediaSource":false},"audio/mpeg; codecs=\\"mp3\\"":{"canPlay":"probably","mediaSource":false},"audio/wav; codecs=\\"0\\"":{"canPlay":"","mediaSource":false},"audio/wav; codecs=\\"2\\"":{"canPlay":"","mediaSource":false},"audio/wave; codecs=\\"0\\"":{"canPlay":"","mediaSource":false},"audio/wave; codecs=\\"1\\"":{"canPlay":"","mediaSource":false},"audio/wave; codecs=\\"2\\"":{"canPlay":"","mediaSource":false},"audio/x-wav; codecs=\\"0\\"":{"canPlay":"","mediaSource":false},"audio/x-wav; codecs=\\"1\\"":{"canPlay":"probably","mediaSource":false},"audio/x-wav; codecs=\\"2\\"":{"canPlay":"","mediaSource":false},"audio/x-pn-wav; codecs=\\"0\\"":{"canPlay":"","mediaSource":false},"audio/x-pn-wav; codecs=\\"1\\"":{"canPlay":"","mediaSource":false},"audio/x-pn-wav; codecs=\\"2\\"":{"canPlay":"","mediaSource":false}}'),
                    },
                    {
                        "key": "video_codecs",
                        "value": '{"ogg":"","h264":"probably","webm":"probably","mpeg4v":"","mpeg4a":"","theora":""}',
                    },
                    {
                        "key": "video_codecs_extended_hash",
                        "value": Arkose().call_ie('{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}}'),
                    },
                    {"key": "media_query_dark_mode", "value": False},
                    {
                        "key": "f9bf2db",
                        "value": '{"pc":"no-preference","ah":"hover","ap":"fine","p":"fine","h":"hover","u":"fast","prm":"no-preference","prt":"no-preference","s":"enabled","fc":"none"}',
                    },
                    {"key": "headless_browser_phantom", "value": False},
                    {"key": "headless_browser_selenium", "value": False},
                    {"key": "headless_browser_nightmare_js", "value": False},
                    {"key": "headless_browser_generic", "value": 4},
                    {"key": "1l2l5234ar2", "value": f"{round(time.time() * 1000)}⁣"},
                    {
                        "key": "document__referrer",
                        "value": "https://accounts.snapchat.com/",
                    },
                    {
                        "key": "window__ancestor_origins",
                        "value": ["https://accounts.snapchat.com"],
                    },
                    {"key": "window__tree_index", "value": [1]},
                    {"key": "window__tree_structure", "value": "[[],[],[]]"},
                    {
                        "key": "window__location_href",
                        "value": "https://iframe.arkoselabs.com/EA4B65CB-594A-438E-B4B5-D0DBA28C9334/lightbox.html",
                    },
                    {
                        "key": "client_config__sitedata_location_href",
                        "value": "https://iframe.arkoselabs.com/EA4B65CB-594A-438E-B4B5-D0DBA28C9334/lightbox.html",
                    },
                    {"key": "client_config__language", "value": "fr-fr"},
                    {
                        "key": "client_config__surl",
                        "value": "https://snap-api.arkoselabs.com",
                    },
                    {"key": "c8480e29a", "value": f"{Arkose().call_ie('https://snap-api.arkoselabs.com')}⁢"},
                    {"key": "client_config__triggered_inline", "value": False},
                    {"key": "mobile_sdk__is_sdk", "value": False},
                    {"key": "audio_fingerprint", "value": "124.04347527516074"},
                    {"key": "navigator_battery_charging", "value": True},
                    {
                        "key": "media_device_kinds",
                        "value": ["audioinput", "videoinput", "audiooutput"],
                    },
                    {
                        "key": "media_devices_hash",
                        "value": "199eba60310b53c200cc783906883c67",
                    },
                    {"key": "1f220c9", "value": "d99a347770ecf166460560b1c06f8e42"},
                    {
                        "key": "math_fingerprint",
                        "value": "0ce80c69b75667d69baedc0a70c82da7",
                    },
                    {
                        "key": "supported_math_functions",
                        "value": "67d1759d7e92844d98045708c0a91c2f",
                    },
                    {"key": "screen_orientation", "value": "landscape-primary"},
                    {"key": "rtc_peer_connection", "value": 5},
                    {
                        "key": "4b4b269e68",
                        "value": "21dafbcb-1ad1-4a45-bcfb-f55afcfd75b8",
                    },
                    {"key": "6a62b2a558", "value": "df45d93b7883fed1e47dedac58c1d924"},
                    {"key": "is_keyless", "value": False},
                    {"key": "c2d2015", "value": "29d13b1af8803cb86c2697345d7ea9eb"},
                    {"key": "43f2d94", "value": []},
                    {"key": "20c15922", "value": True},
                    {"key": "4f59ca8", "value": None},
                    {
                        "key": "3ea7194",
                        "value": {
                            "supported": True,
                            "formats": ["HDR10", "HLG"],
                            "isHDR": False,
                        },
                    },
                    {"key": "05d3d24", "value": "7bd8fe2b950ecd77778f4bf4c2c1b213"},
                    {
                        "key": "speech_default_voice",
                        "value": "Microsoft Hortense - French (France) || fr-FR",
                    },
                    {
                        "key": "speech_voices_hash",
                        "value": "454fcd9268dcabe2bbed64359fff08b1",
                    },
                    {"key": "83eb055", "value": False},
                    {"key": "4ca87df3d1", "value": b64encode(";".encode()).decode()},
                    {"key": "867e25e5d4", "value": b64encode(";".encode()).decode()},
                    {"key": "d4a306884c", "value": b64encode(";".encode()).decode()},
                ],
            },
            {
                "key": "fe",
                "value": fe,
            },
            {"key": "ife_hash", "value": self.call_d(", ".join(fe), 38)},
            {
                "key": "jsbd",
                "value": '{"HL":3,"NCE":True,"DT":"Authentication","NWD":"False","DMTO":1,"DOTO":1}',
            },
        ]

    def get_bda(self):
        iv = get_random_bytes(16)
        salt = get_random_bytes(8)
        fingerprint = bytes(json.dumps(self.get_fingerprint()), "utf-8")

        Ot_raw = ctx.call(
            "nn",
            f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36{self.ark_esync_value}",
            salt.hex(),
        )
        Ot = bytes([Ot_raw[str(i)] for i in range(len(Ot_raw))])

        cipher = AES.new(Ot, AES.MODE_CBC, iv)
        ct = cipher.encrypt(pad(fingerprint, AES.block_size))
        ct = "".join([chr(c) for c in ct])

        return b64encode(
            json.dumps(
                {"ct": b64encode(ct.encode()).decode(), "s": salt.hex(), "iv": iv.hex()}
            ).encode()
        ).decode()

Arkose().get_bda()