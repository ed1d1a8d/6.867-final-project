import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data_utils
from get_data import get_audio_and_speakers
from model import LSTMVoice, dtype

NUM_PEOPLE = 10

audio, speaker = get_audio_and_speakers(NUM_PEOPLE)

total_dataset_size = len(audio)

train_size = total_dataset_size // 2
val_size = total_dataset_size // 4

audio_train = torch.FloatTensor(audio[:train_size])
speaker_train = torch.IntTensor(speaker[:train_size])

audio_val = torch.FloatTensor(audio[train_size : train_size + val_size])
speaker_val = torch.IntTensor(speaker[train_size : train_size + val_size])

audio_test = torch.FloatTensor(audio[train_size + val_size:])
speaker_test = torch.IntTensor(speaker[train_size + val_size:])


train = data_utils.TensorDataset(audio_train, speaker_train)
train_loader = data_utils.DataLoader(train, batch_size=64, shuffle=True)


def evaluate(model, audio, speaker):
    data = data_utils.TensorDataset(audio, speaker)
    data_loader = data_utils.DataLoader(data, batch_size=64, shuffle=True)

    correct = 0
    total = 0
    for i, batch in enumerate(data_loader, 0):
        inputs, labels = batch
        if inputs.shape[0] != 64:
            continue
        total += 64

        inputs = inputs.permute(2, 0, 1)
        inputs = autograd.Variable(inputs.type(dtype))
        scores = model(inputs).data
        for i, x in enumerate(scores):
            j = max(range(len(x)), key=lambda j: x[j])
            if j == labels[i]:
                correct += 1

    return correct * 1.0 / total

INPUT_DIM = 128
HIDDEN_DIM = 256
DEPTH = 1
BATCH_SIZE = 64


model = LSTMVoice(INPUT_DIM, HIDDEN_DIM, DEPTH, BATCH_SIZE, NUM_PEOPLE)
model = model.cuda()

loss_function = nn.NLLLoss()
optimizer = optim.RMSprop(model.parameters(), lr=0.01)

losses = []
running_loss = 0.0

NUM_EPOCHS = 5
for epoch in range(NUM_EPOCHS):
    print('training epoch', epoch+1)
    running_loss = 0.0
    for i, data in enumerate(train_loader, 0):
        inputs, labels = data
        if inputs.shape[0] != 64:
            continue
        inputs = inputs.permute(2, 0, 1)

        inputs = autograd.Variable(inputs.type(dtype))
        labels = autograd.Variable(labels.type(dtype).long())

        model.zero_grad()

        scores = model(inputs)
        loss = loss_function(scores, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        losses += [loss.data[0]]
        running_loss += loss.data[0]
        if i % 100 == 99:    # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 100))
            running_loss = 0.0

print("Train:", evaluate(model, audio_train, speaker_train))
print("Val:", evaluate(model, audio_val, speaker_val))
print("Test:", evaluate(model, audio_test, speaker_test))
