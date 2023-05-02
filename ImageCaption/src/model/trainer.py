'''
    Module contains Trainer used in training and testing processes.
'''

import io
import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

import torch
from tqdm import tqdm


class Trainer:
    def __init__(
            self,
            model,
            optimizer,
            scaler,
            scheduler,
            train_loader,
            valid_loader,
            test_dataset='./data',
            test_path='',
            ckp_path='',
            device='cpu'
    ):
        self.model = model
        self.optimizer = optimizer
        self.scaler = scaler
        self.scheduler = scheduler
        self.train_loader = train_loader
        self.valid_loader = valid_loader
        self.test_dataset = test_dataset
        self.test_path = test_path
        self.ckp_path = ckp_path
        self.device = device

        # load checkpoint
        if os.path.isfile(ckp_path):
            self._load_ckp(
                ckp_path,
                optimizer=optimizer,
                scheduler=scheduler,
                scaler=scaler,
                epoch=True,
                train_loss=True,
                valid_loss=True,
                device=device
            )

        else:
            self.cur_lr = self.optimizer.param_groups[0]['lr']
            self.epoch = 0
            self.train_loss = []
            self.valid_loss = []
            self.test_result = None

    def train_epoch(self):
        self.model.train()
        self.epoch += 1

        total_loss = 0

        loop = tqdm(self.train_loader, total=len(self.train_loader))
        loop.set_description(f'Epoch: {self.epoch} | Loss: ---')
        for batch_idx, (img_emb, cap, att_mask) in enumerate(loop):
            img_emb, cap, att_mask = img_emb.to(self.device), cap.to(self.device), att_mask.to(self.device)

            with torch.cuda.amp.autocast():
                loss = self.model.train_forward(img_emb=img_emb, trg_cap=cap, att_mask=att_mask)

            self.scaler.scale(loss).backward()
            self.scaler.unscale_(self.optimizer)

            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.3)

            self.scaler.step(self.optimizer)
            self.scaler.update()

            self.optimizer.zero_grad()

            total_loss += loss.item()

            loop.set_description(f'Epoch: {self.epoch} | Loss: {total_loss / (batch_idx + 1):.3f}')
            loop.refresh()

        self.cur_lr = self.optimizer.param_groups[0]['lr']
        self.train_loss.append(total_loss / (batch_idx + 1))

        self.scheduler.step()

    def valid_epoch(self):
        self.model.eval()

        total_loss = 0

        loop = tqdm(self.valid_loader, total=len(self.valid_loader))
        loop.set_description(f'Validation Loss: ---')
        for batch_idx, (img_emb, cap, att_mask) in enumerate(loop):
            img_emb, cap, att_mask = img_emb.to(self.device), cap.to(self.device), att_mask.to(self.device)

            with torch.no_grad():
                with torch.cuda.amp.autocast():
                    loss = self.model.train_forward(img_emb=img_emb, trg_cap=cap, att_mask=att_mask)

                    total_loss += loss.item()

                    loop.set_description(f'Validation Loss: {total_loss / (batch_idx + 1):.3f}')
                    loop.refresh()

        self.valid_loss.append(total_loss / (batch_idx + 1))