import pandas as pd
from src.data import make_dataset
from src.features import build_features
from src.utils import utils
from src.data import cluster
import os


def create_dataset(start_year, end_year, dataset, num, method='cluster', time_div=False):
    parameters = {
        # Relative file path to raw data sets (should be named year.csv and also contain trigram vec file)
        'data_path': './data/raw/{}_cluster/'.format(dataset),

        # Year to start from
        'start_year': start_year,

        # Year to make prediction for
        'end_year': end_year,

        # 'random' (no clustering), 'hierarchy' or 'dbscan'
        'clustering_method': method,

        # Number of strains sampled for training
        'training_samples': 800,

        # Number of strains sampled for validation
        'testing_samples': 200,

        # File name to give the created data set (will be appended by clustering method and train/test)
        'file_name': './data/processed/{}_T{}_{}/{}/triplet_'.format(dataset, end_year - start_year, end_year, num)
    }

    directory = parameters['file_name'][:-9]
    if os.path.exists(directory):
        return
    else:
        os.makedirs(directory)

    # RBD sites
    if dataset == 'Covid':
        positions = [332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350,
                     351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369,
                     370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388,
                     389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407,
                     408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426,
                     427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445,
                     446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464,
                     465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483,
                     484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502,
                     503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521,
                     522, 523, 524, 525, 526]
        positions.sort()

    # Epitopes sites for the H1 protein
    if dataset == 'H1N1':
        epitope_a = [118, 120, 121, 122, 126, 127, 128, 129, 132, 133, 134, 135, 137, 139, 140, 141, 142, 143, 146, 147,
                     149, 165, 252, 253]
        epitope_b = [124, 125, 152, 153, 154, 155, 156, 157, 160, 162, 163, 183, 184, 185, 186, 187, 189, 190, 191, 193,
                     194, 196]
        epitope_c = [34, 35, 36, 37, 38, 40, 41, 43, 44, 45, 269, 270, 271, 272, 273, 274, 276, 277, 278, 283, 288, 292,
                     295, 297, 298, 302, 303, 305, 306, 307, 308, 309, 310]
        epitope_d = [89, 94, 95, 96, 113, 117, 163, 164, 166, 167, 168, 169, 170, 171, 172, 173, 174, 176, 179, 198,
                     200, 202, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 222, 223, 224, 225, 226,
                     227, 235, 237, 239, 241, 243, 244, 245]
        epitope_e = [47, 48, 50, 51, 53, 54, 56, 57, 58, 66, 68, 69, 70, 71, 72, 73, 74, 75, 78, 79, 80, 82, 83, 84, 85,
                     86, 102, 257, 258, 259, 260, 261, 263, 267]
        positions = epitope_a + epitope_b + epitope_c + epitope_d + epitope_e
        positions.sort()
        # epitope_positions = [118]

    # Epitopes sites for the H3 subtype
    if dataset == 'H3N2':
        epitope_a = [122, 124, 126, 130, 131, 132, 133, 135, 136, 137, 138, 140, 142, 143, 144, 145, 146, 150, 152, 168]
        epitope_b = [128, 129, 155, 156, 157, 158, 159, 160, 163, 165, 186, 187, 188, 189, 190, 192, 193, 194, 196, 197,
                     198]
        epitope_c = [44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 273, 275, 276, 278, 279, 280, 294, 297, 299, 300, 304, 305,
                     307, 308, 309, 310, 311, 312]
        epitope_d = [96, 102, 103, 117, 121, 167, 170, 171, 172, 173, 174, 175, 176, 177, 179, 182, 201, 203, 207, 208,
                     209, 212, 213, 214, 215, 216, 217, 218, 219, 226, 227, 228, 229, 230, 238, 240, 242, 244, 246, 247,
                     248]
        epitope_e = [57, 59, 62, 63, 67, 75, 78, 80, 81, 82, 83, 86, 87, 88, 91, 92, 94, 109, 260, 261, 262, 265]
        positions = epitope_a + epitope_b + epitope_c + epitope_d + epitope_e
        positions.sort()

    # Epitopes sites for the H5 protein
    if dataset == 'H5N1':
        positions = [36, 48, 53, 55, 56, 57, 62, 65, 71, 77, 78, 80, 81, 82, 83, 84, 86, 87, 91, 94, 115, 116,
                     117, 118, 119,
                     120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 133, 136, 138, 140, 141, 142,
                     143, 144, 145,
                     149, 150, 151, 152, 153, 154, 155, 156, 157, 159, 160, 161, 162, 163, 164, 165, 166, 167,
                     168, 169, 171,
                     172, 173, 174, 179, 182, 185, 186, 187, 189, 190, 191, 193, 200, 205, 206, 207, 212, 222,
                     226, 230, 242,
                     244, 245, 246, 252, 256, 259, 261, 262, 263, 273, 274, 276, 278, 282]
        # epitope_positions = np.unique(epitope_positions)
        positions.sort()

    years = list(range(parameters['start_year'], parameters['end_year'] + 1))
    data_files = list(map(lambda x: str(x) + '.csv', years))
    test_split = parameters['testing_samples'] / (parameters['training_samples'] + parameters['testing_samples'])

    trigram_to_idx, _ = make_dataset.read_trigram_vecs(parameters['data_path'])

    strains_by_year = make_dataset.read_strains_from(data_files, parameters['data_path'])

    train_strains_by_year, test_strains_by_year = make_dataset.train_test_split_strains(strains_by_year, test_split,
                                                                                        parameters['clustering_method'])

    if parameters['clustering_method'] != 'random':
        if parameters['clustering_method'] == 'cluster':
            train_strains_by_year = build_features.sample_strains_cluster(train_strains_by_year,
                                                                          parameters['training_samples'])
            test_strains_by_year = build_features.sample_strains_cluster(test_strains_by_year,
                                                                         parameters['testing_samples'])
        else:
            train_strains_by_year, train_clusters_by_year = utils.cluster_years(train_strains_by_year,
                                                                                parameters['data_path'],
                                                                                parameters['clustering_method'])
            test_strains_by_year, test_clusters_by_year = utils.cluster_years(test_strains_by_year,
                                                                              parameters['data_path'],
                                                                              parameters['clustering_method'])

            train_strains_by_year = cluster.sample_from_clusters(train_strains_by_year, train_clusters_by_year,
                                                                 parameters['training_samples'])
            test_strains_by_year = cluster.sample_from_clusters(test_strains_by_year, test_clusters_by_year,
                                                                parameters['testing_samples'])

    else:
        train_strains_by_year = build_features.sample_strains(train_strains_by_year, parameters['training_samples'])
        test_strains_by_year = build_features.sample_strains(test_strains_by_year, parameters['testing_samples'])

    create_triplet_trigram_dataset(train_strains_by_year, trigram_to_idx, positions,
                                   file_name=(parameters['file_name'] + parameters['clustering_method'] + '_train'))
    create_triplet_trigram_dataset(test_strains_by_year, trigram_to_idx, positions,
                                   file_name=(parameters['file_name'] + parameters['clustering_method'] + '_test'))


def create_triplet_trigram_dataset(strains_by_year, trigram_to_idx, epitope_positions, file_name):
    """Creates a dataset in csv format.
    X: Time series of three overlapping trigram vectors, one example for each epitope.
    Y: 0 if epitope does not mutate, 1 if it does.
    """
    triplet_strains_by_year = build_features.make_triplet_strains(strains_by_year, epitope_positions)
    trigrams_by_year = build_features.split_to_trigrams(triplet_strains_by_year)
    trigram_idxs = build_features.map_trigrams_to_idxs(trigrams_by_year, trigram_to_idx)
    labels = build_features.make_triplet_labels(triplet_strains_by_year)

    acc, p, r, f1, mcc = build_features.get_majority_baselines(triplet_strains_by_year, labels)
    with open(file_name + '_baseline.txt', 'w') as f:
        f.write(' Accuracy:\t%.3f\n' % acc)
        f.write(' Precision:\t%.3f\n' % p)
        f.write(' Recall:\t%.3f\n' % r)
        f.write(' F1-score:\t%.3f\n' % f1)
        f.write(' Matthews CC:\t%.3f' % mcc)

    data_dict = {'y': labels}
    for year in range(len(triplet_strains_by_year) - 1):
        data_dict[year] = trigram_idxs[year]

    pd.DataFrame(data_dict).to_csv(file_name + '.csv', index=False)
