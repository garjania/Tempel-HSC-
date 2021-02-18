import argparse
from torch.utils.data import DataLoader
from model import Classifier
from src.models.models import AttentionModel
from src.scripts.create_dataset import create_dataset
from loader import load_datasets
import os
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='H5N1')
parser.add_argument('--start_year', type=int, default=2001)
parser.add_argument('--end_year', type=int, default=2016)
parser.add_argument('--create_dataset', type=bool, default=False)
parser.add_argument('--train', type=bool, default=True)
args = parser.parse_args()

PATHS = {'train': './data/processed/{}_T{}_{}/{}/triplet_dbscan_train.csv',
         'test': './data/processed/{}_T{}_{}/{}/triplet_dbscan_test.csv',
         'result': './results/{}_T{}_{}'}

parameters = {
    'hidden_size': 128,

    'dropout_p': 0.5,

    'learning_rate': 0.001,

    'batch_size': 256,

    'input_dim': 100,

    'num_of_epochs': 50,

    'lr_milestones': [25]
}

dataset_features = {
    'dataset': args.dataset,

    'num_of_datasets': 5,

    'start_year': args.start_year,

    'end_year': args.end_year,
}

if __name__ == '__main__':
    if args.create_dataset:
        for i in range(dataset_features['num_of_datasets']):
            create_dataset(dataset_features['start_year'], dataset_features['end_year'], dataset_features['dataset'], i + 1)
    if args.train:
        res_path = PATHS['result'].format(dataset_features['dataset'],
                                          dataset_features['end_year'] -
                                          dataset_features['start_year'],
                                          dataset_features['end_year'])
        if not os.path.exists(res_path):
            os.mkdir(res_path)
        final_res = {'mean': {'precision': 0, 'recall': 0, 'f-score': 0, 'mcc': 0, 'accuracy': 0, 'auc': 0},
                     'var': {'precision': 0, 'recall': 0, 'f-score': 0, 'mcc': 0, 'accuracy': 0, 'auc': 0}}
        for i in range(dataset_features['num_of_datasets']):
            train_dataset, valid_dataset, test_dataset = load_datasets(dataset_features['dataset'],
                                                                       PATHS['train'].format(dataset_features['dataset'],
                                                                                             dataset_features['end_year'] -
                                                                                             dataset_features['start_year'],
                                                                                             dataset_features['end_year'],
                                                                                             i + 1),
                                                                       PATHS['test'].format(dataset_features['dataset'],
                                                                                            dataset_features['end_year'] -
                                                                                            dataset_features['start_year'],
                                                                                            dataset_features['end_year'],
                                                                                            i + 1))

            train_loader = DataLoader(
                dataset=train_dataset,
                batch_size=parameters['batch_size'], shuffle=True, drop_last=True)
            val_loader = DataLoader(
                dataset=valid_dataset,
                batch_size=parameters['batch_size'], shuffle=False, drop_last=False)
            test_loader = DataLoader(
                dataset=test_dataset,
                batch_size=parameters['batch_size'], shuffle=False, drop_last=False)

            seq_length = dataset_features['end_year'] - dataset_features['start_year'] - 1
            net = AttentionModel(seq_length, parameters['input_dim'], parameters['hidden_size']
                                 , parameters['dropout_p']).float()
            classifier = Classifier(batch_size=parameters['batch_size'], lr_milestones=parameters['lr_milestones']
                                    , n_epochs=parameters['num_of_epochs'])
            classifier.train(net, train_loader, test_loader, val_loader)

            df = pd.DataFrame.from_dict(classifier.scores)
            df.to_csv(res_path + '/{}.csv'.format(i + 1))
            for k, v in classifier.scores['test'].items():
                final_res['mean'][k] = (final_res['mean'][k] * i + sum(v) / len(v)) / (i + 1)
            for k, v in classifier.scores['test'].items():
                final_res['var'][k] = (i * (final_res['mean'][k] - sum(v) / len(v)) ** 2 + final_res['var'][k]) / (i + 1)
        df = pd.DataFrame.from_dict(final_res)
        df.to_csv(res_path + '/final.csv')
