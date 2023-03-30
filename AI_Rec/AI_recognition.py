from PIL import Image, ImageDraw
import torchvision
from torchvision.io import ImageReadMode
import plotly.express as px
import torch
from linformer import Linformer
from torchvision import datasets, transforms
from vit_pytorch.efficient import ViT

try:
    from . import labels_map
except Exception:
    import labels_map


class AIRec():
    def __init__(self, ViT_path='./AI_Rec/ViTmodel/ViTmodel.pth'):
        self.device = 'cpu'
        print(f"Torch: {torch.__version__}, using cpu for compatibility")
        self.ViTTransforms = transforms.Compose(
            [
                # transforms.ToPILImage(),
                # transforms.Resize(256),
                transforms.Resize((224, 224)),
                # transforms.CenterCrop(224),
                transforms.ToTensor(),
            ]
        )
        efficient_transformer = Linformer(
            dim=128,
            seq_len=49 + 1,  # 7x7 patches + 1 cls-token
            depth=12,
            heads=8,
            k=64
        )
        self.ViT_model = ViT(
            dim=128,
            image_size=224,
            patch_size=32,
            num_classes=34,
            transformer=efficient_transformer,
            channels=3,
        ).to(self.device)  # all CPU inference
        self.ViT_model.load_state_dict(torch.load(
            ViT_path, map_location=torch.device('cpu')))
        self.ViT_model.eval()
        self.rcnn_model = torchvision.models.detection.fasterrcnn_resnet50_fpn_v2(
            weights="DEFAULT").to(self.device)
        self.rcnn_model.eval()

    def _RCNN(self, img_pil, detection_threshold=0.5):
        ###
        # take pil img as input
        # #
        img_in = torchvision.transforms.functional.to_tensor(img_pil)
        img_in = torch.unsqueeze(img_in, dim=0)
        rcnn_out = self.rcnn_model(img_in)
        print(rcnn_out[0]['boxes'].shape)
        print(rcnn_out[0]['labels'].shape)
        print(rcnn_out[0]['scores'].shape)
        out = []
        for box, label, score in zip(rcnn_out[0]['boxes'], rcnn_out[0]['labels'], rcnn_out[0]['scores']):
            if score > detection_threshold:
                out.append((box, label, score))
        return out

    def _ViT(self, img, classification_threshold=0.2):
        ###
        # take a pil img, do inference.
        # #
        img = self.ViTTransforms(img)
        img = torch.unsqueeze(img, dim=0)
        ViT_out = self.ViT_model(img)
        sf_output = torch.nn.functional.softmax(ViT_out)
        top3 = torch.topk(sf_output, k=3)
        top3_ls = top3.indices.cpu().numpy().tolist()[0]
        top3_str = list(map(lambda x: labels_map.labels_map[x], top3_ls))
        top3_val = top3.values.cpu().detach().numpy().tolist()[0]
        top3_val = [round(x, 2) for x in top3_val]
        if top3_val[0] > classification_threshold:
            print(top3_str, top3_val)
            return (top3_str, top3_val)
        else:
            return None

    def load_pil_img(self, img_path):
        ###
        # return a img pil
        # ###
        img = torchvision.io.read_image(
            img_path, ImageReadMode.RGB).to(self.device)
        img_pil = torchvision.transforms.functional.to_pil_image(img)
        return img_pil

    def pil_to_tensor(self, img_pil):
        img = torchvision.transforms.functional.to_tensor(
            img_pil).to(self.device)
        return img

        # img_in = torch.unsqueeze(img_in, dim=0)

    def save_pil_img(self, img_pil, path='./AI_Rec/imgs/tmp.png'):
        img_pil.save(path)

    def show_pil_img(self, img):
        img.show()

    def show_tensor_img(self, img):
        fig = px.imshow(img.permute((1, 2, 0)).cpu().numpy())
        fig.show()

    def draw_box_output(self, img_pil, box_list):
        ###
        # box_list = [] # [[box,score,top3_str,top3_val],]
        ###
        with torch.no_grad():
            image = img_pil.copy()
            draw = ImageDraw.Draw(image)

            for box, score, top3_str, top3_val in box_list:
                x, y, w, h = tuple(box)
                draw.rectangle((x, y, w, h), outline="red", width=1)
                draw.text(
                    (x, y), f'score:{score}\ntop3:{top3_str},\ntop3_val={top3_val}', fill="blue")
                print(f'score:{score}\ntop3:{top3_str},\ntop3_val={top3_val}')
            return image

    def box_list_to_text_list(self, box_list):
        txt_list = []
        with torch.no_grad():
            for box, score, top3_str, top3_val in box_list:
                x, y, w, h = tuple(box)
                txt_list.append(f'score:{score}\ntop3:{top3_str},\ntop3_val={top3_val}')
            return txt_list

    def inference(self, img_pil):
        ###
        # perform inference in one pil img
        # #
        rcnn_out = self._RCNN(img_pil)

        box_list = []  # [[box,score,top3_str,top3_val],]
        with torch.no_grad():
            for box, label, score in rcnn_out:
                x, y, w, h = box.numpy()
                w = w - x
                h = h - y
                cropped_img = transforms.functional.crop(
                    img_pil, y, x, h, w)  # node torch x y flipped
                # img.show()
                ViT_out = self._ViT(cropped_img)
                if ViT_out is not None:
                    box_list.append([box, score, ViT_out[0], ViT_out[1]])
        print(box_list)
        return box_list


if __name__ == "__main__":
    AI = AIRec()
    img = AI.load_pil_img('./AI_Rec/imgs/redbull.jpg')
    box_list = AI.inference(img)
    img_pil = AI.draw_box_output(img, box_list)
    AI.show_pil_img(img_pil)
    AI.save_pil_img(img_pil, './AI_Rec/imgs/out.png')
