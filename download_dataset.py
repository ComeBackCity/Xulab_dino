import gdown

if __name__ == "__main__":
    # url = "https://drive.google.com/file/d/1MIoSVvFAa35mQTEKsEGJUqPa5tO8hk-o/view?usp=sharing"
    # url = "https://drive.google.com/file/d/1w40yYhtLWb3w7nuPcXwpctdK_Oc3k4JZ/view?usp=drive_link"
    id = "1w40yYhtLWb3w7nuPcXwpctdK_Oc3k4JZ"
    output = "dataset_no_contrast.zip"
    gdown.download(id=id, output=output, quiet=True)