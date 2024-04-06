import modules.scripts as scripts
import gradio as gr

from modules.processing import StableDiffusionProcessing

class Classification():
    def __init__(self, name, inf, pos, neg, en):
        self.name = name
        self.info = inf
        self.positive = pos
        self.negative = neg
        self.enabled = en

    def ui(self):
        with gr.Blocks():
            with gr.Accordion(self.name, open = self.enabled):
                with gr.Row():
                    _enabled = gr.Checkbox(True, label = "Enable", info = self.info)
                with gr.Row():
                    with gr.Column():
                        _positive_enabled = gr.Checkbox(self.enabled, label = "Positive Prompt")
                        _positive_textbox = gr.Textbox(label = "", lines = 3, value = self.positive)
                    with gr.Column():
                        _negative_enabled = gr.Checkbox(self.enabled, label = "Negative Prompt")
                        _negative_textbox = gr.Textbox(label = "", lines = 3, value = self.negative)
        return _enabled, _positive_enabled, _positive_textbox, _negative_enabled, _negative_textbox

class Classifications():
    def __init__(self):
        self.classifications = []
    def add(self, name, info, positive, negative, enabled):
        cf = Classification(name, info, positive, negative, enabled)
        self.classifications.append(cf)
    def ui(self):
        r = []
        for cf in self.classifications:
            with gr.Row():
                u = cf.ui()
            r.append(u)
        return r

class ExtensionTemplateScript(scripts.Script):
    def __init__(self):
        cfs = Classifications()
        cfs.add(
                name = "品質",
                info = "",
                positive = "masterpiece, ultra detailed, ",
                negative = "(low quality, worst quality, lips:1.4), ",
                enabled = True,
                )
        cfs.add(
                name = "作風",
                info = "絵の雰囲気・タッチ",
                positive = "",
                negative = "",
                enabled = True,
                )
        cfs.add(
                name = "主題",
                info = "作画対象",
                positive = "1 girl, ",
                negative = "",
                enabled = True,
                )
        cfs.add(
                name = "顔",
                info = "",
                positive = "",
                negative = "",
                enabled = True,
                )
        cfs.add(
                name = "髪",
                info = "",
                positive = "",
                negative = "",
                enabled = True,
                )
        cfs.add(
                name = "表情",
                info = "",
                positive = "",
                negative = "",
                enabled = True,
                )
        cfs.add(
                name = "身体",
                info = "体格",
                positive = "",
                negative = "",
                enabled = True,
                )
        cfs.add(
                name = "服装",
                info = "",
                positive = "",
                negative = "",
                enabled = True,
                )
        cfs.add(
                name = "装飾",
                info = "鞄・汗",
                positive = "",
                negative = "",
                enabled = True,
                )
        cfs.add(
                name = "ポーズ",
                info = "",
                positive = "",
                negative = "",
                enabled = True,
                )
        cfs.add(
                name = "構図",
                info = "",
                positive = "",
                negative = "",
                enabled = True,
                )
        cfs.add(
                name = "背景",
                info = "",
                positive = "",
                negative = "",
                enabled = True,
                )
        self.classifications = cfs

    def title(self):
        return "Prompt Organizer"
    def show(self, is_img2img):
        return scripts.AlwaysVisible
    def ui(self, is_img2img):
        with gr.Accordion(self.title(), open = False):
            with gr.Tab("General"):
                with gr.Row():
                    enabled = gr.Checkbox(False, label="Enable")
                with gr.Row():
                    self.classifications.ui()
            with gr.Tab("Example", visible = False):
                with gr.Row():
                    enabled = gr.Checkbox(False, label="Enable")
                    ret = self.classifications.ui()
        return [enabled, ret]

    def list2string(self, lis):
        pts = ""
        nts = ""
        for li in lis:
            if li[0]:
                if li[1]:
                    pts = pts.join(li[2])
                if li[3]:
                    nts = nts.join(li[4])
        return pts, nts

    def process(self, p: StableDiffusionProcessing, enabled, ret):
        if not enabled:
            return
        prePositive, preNegative = self.list2string(ret)
        prompt = p.prompt
        negative_prompt = p.negative_prompt
        if prePositive:
           prompt = prePositive + ", " + prompt
        if postPositive:
           prompt = prompt + ", " + postPositive
        if preNegative:
           negative_prompt = preNegative + ", " + negative_prompt
        if postNegative:
           negative_prompt = negative_prompt + ", " + postNegative
        p.all_prompts[0] = prompt
        p.all_negative_prompts[0] = negative_prompt

