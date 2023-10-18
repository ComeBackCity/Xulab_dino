import json
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import numpy as np
import os

def train_plot_loss(max_epochs, out_dir):
    path = f"output/log.txt"
    losses, lr = [], []
    with open(path, "r") as f:
        for line in f:
            metric_map = json.loads(line)
            losses.append(metric_map["train_loss"])
            lr.append(metric_map["train_lr"])

    epochs = min(max_epochs, len(losses))
    dir = f"metric_plots/{out_dir}"
    os.makedirs(dir, exist_ok=True)

    plt.style.use("ggplot")
    loss_plt = sns.lineplot(x=range(0, epochs, 1), y=losses[:epochs])
    fig = loss_plt.get_figure()
    fig.savefig(f"{dir}/loss_epochs_{epochs}.jpg", dpi=1200)
    plt.close()

    plt.style.use("ggplot")
    lr_plt = sns.lineplot(x=range(0, epochs, 1), y=lr[:epochs])
    fig = lr_plt.get_figure()
    fig.savefig(f"{dir}/lr_epochs_{epochs}.jpg", dpi=1200)
    plt.close()

if __name__ == "__main__":
    epochs = int(sys.argv[1])
    out_dir = sys.argv[2]

    train_plot_loss(epochs, out_dir)

