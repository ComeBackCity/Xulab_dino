import gdown

if __name__ == "__main__":
    # https://drive.google.com/file/d/1s3V9QH8LatIl4KMMDIP5wcKY5qeOs66p/view?usp=sharing
    # https://drive.google.com/file/d/1RQ8DijdHRjj5BT2HTT_-RDzLdoTRng4w/view?usp=share_link
    # 1klhtjrNtvoqvfna2ievGMaoEJ5mIQ3BT
    # https://drive.google.com/file/d/1klhtjrNtvoqvfna2ievGMaoEJ5mIQ3BT/view?usp=sharing
    # https://drive.google.com/file/d/1JrE6WJt185_-lfF-SnaIz4kQVVwR4WbH/view?usp=sharing
    # id = "1JrE6WJt185_-lfF-SnaIz4kQVVwR4WbH"
    # https://drive.google.com/file/d/1xx7sJPg8v_ijxbPk6AwrISsks6stevEW/view?usp=sharing
    id = "1xx7sJPg8v_ijxbPk6AwrISsks6stevEW"
    output = "dataset_mito.zip"
    gdown.download(id=id, output=output, quiet=True)
