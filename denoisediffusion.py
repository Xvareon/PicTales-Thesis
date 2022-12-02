# IMPORT THE LIBRARY OF DDPM, saves the trouble of cloning the whole repo
from denoising_diffusion_pytorch import Unet, GaussianDiffusion, Trainer
import os
import sys

if __name__ == '__main__':
    model = Unet(  # Model Flags and Hyperparameters
        dim=64,                     # dimension limit
        dim_mults=(1, 2, 4, 8)      # hyperbolic dims
    ).cuda()

    diffusion = GaussianDiffusion(  # Diffusion Flags and Hyperparameters
        model,
        image_size=128,           # Image size for diffusing
        timesteps=1000,           # number of steps

        # number of sampling timesteps (using ddim for faster inference [see citation for ddim paper])
        sampling_timesteps=250,
        loss_type='l1'            # L1 or L2
    ).cuda()

    trainer = Trainer(  # Train Flags and Hyperparameters
        diffusion,
        './dataset/flickr30k_images/',  # DATASET FOLDER
        train_batch_size=16,            # DEFAULT: 32
        train_lr=8e-5,                  # Formula that I don't know but it works
        train_num_steps=1000,           # total training steps DEFAULT: 700000
        gradient_accumulate_every=2,    # gradient accumulation steps
        ema_decay=0.995,                # exponential moving average decay
        amp=True                        # turn on mixed precision
    )
    file_count = sum(len(files)
                     for _, _, files in os.walk('./dataset/flickr30k_images/'))
    if (file_count <= 4000):
        print("Insufficient data in dataset!")
        sys.exit(0)
    trainer.train()     # RUN THE TRAINING, WILL STOP WHEN IT PRINTS IN THE TERMINAL: "training complete!, OUTPUTS A PT FILE named 'model-1.pt' in the results folder"
