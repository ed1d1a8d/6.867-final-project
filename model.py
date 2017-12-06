# Based off of http://pytorch.org/tutorials/beginner/nlp/sequence_models_tutorial.html
class LSTMVoice(nn.Module):

    def __init__(self, input_dim, hidden_dim, depth, batch_size, num_labels):
        super(LSTMVoice, self).__init__()
        self.hidden_dim = hidden_dim
        self.input_dim = input_dim
        self.depth = depth
        self.batch_size = batch_size
        self.num_labels = num_labels
        
        self.lstm = nn.LSTM(input_dim, hidden_dim, depth)
        self.fc = nn.Linear(hidden_dim, num_labels)
        self.hidden = self.init_hidden()

    def init_hidden(self):
        # (num_layers, batch_size, hidden_dim)
        return (autograd.Variable(torch.zeros(self.depth, self.batch_size, self.hidden_dim).type(dtype)),
                autograd.Variable(torch.zeros(self.depth, self.batch_size, self.hidden_dim).type(dtype)))

    def forward(self, batch):
        lstm_out, _ = self.lstm(batch, self.hidden)
        lstm_out_mean = torch.mean(lstm_out, 0)
        label_space = self.fc(lstm_out_mean)
        scores = nn.functional.log_softmax(label_space)
        return scores

