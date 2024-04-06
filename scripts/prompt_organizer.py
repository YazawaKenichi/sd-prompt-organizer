import modules.scripts as scripts
import gradio as gr

from modules.processing import StableDiffusionProcessing

def classification(name, info, positive, negative, enabled):
    with gr.Row():
        with gr.Accordion(name, open = enabled):
            with gr.Row():
                _enabled = gr.Checkbox(True, label = "Enable", info = info)
            with gr.Row():
                with gr.Column():
                    _positive_enabled = gr.Checkbox(enabled, label = "Positive Prompt")
                    _positive_textbox = gr.Textbox(label = "", lines = 3, value = positive)
                with gr.Column():
                    _negative_enabled = gr.Checkbox(enabled, label = "Negative Prompt")
                    _negative_textbox = gr.Textbox(label = "", lines = 3, value = negative)
    return _enabled, _positive_enabled, _positive_textbox, _negative_enabled, _negative_textbox

class ExtensionTemplateScript(scripts.Script):
    def title(self):
        return "Prompt Organizer"
    def show(self, is_img2img):
        return scripts.AlwaysVisible
    def categorize(self):
        ret = []
        ret[0] = classification(
                name = "品質",
                info = "",
                positive = "masterpiece, ultra detailed, ",
                negative = "(low quality, worst quality, lips:1.4), ",
                enabled = True,
                )
        ret[1] = classification(
                name = "作風",
                info = "絵の雰囲気・タッチ",
                positive = "",
                negative = "",
                enabled = True,
                )
        ret[2] = classification(
                name = "主題",
                info = "作画対象",
                positive = "1 girl, ",
                negative = "",
                enabled = True,
                )
        ret[3] = classification(
                name = "顔",
                info = "",
                positive = "",
                negative = "",
                enabled = True,
                )
        ret[4] = classification(
                name = "髪",
                info = "",
                positive = "",
                negative = "",
                enabled = True,
                )
        ret[5] = classification(
                name = "表情",
                info = "",
                positive = "",
                negative = "",
                enabled = True,
                )
        ret[6] = classification(
                name = "身体",
                info = "体格",
                positive = "",
                negative = "",
                enabled = True,
                )
        ret[7] = classification(
                name = "服装",
                info = "",
                positive = "",
                negative = "",
                enabled = True,
                )
        ret[8] = classification(
                name = "装飾",
                info = "鞄・汗",
                positive = "",
                negative = "",
                enabled = True,
                )
        ret[9] = classification(
                name = "ポーズ",
                info = "",
                positive = "",
                negative = "",
                enabled = True,
                )
        ret[10] = classification(
                name = "構図",
                info = "",
                positive = "",
                negative = "",
                enabled = True,
                )
        ret[11] = classification(
                name = "背景",
                info = "",
                positive = "",
                negative = "",
                enabled = True,
                )
        return ret

    def ui(self, is_img2img):
        with gr.Accordion(self.title(), open = False):
            with gr.Tab("General"):
                with gr.Row():
                    enabled = gr.Checkbox(False, label="Enable")
                with gr.Row():
                    self.categorize()
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

