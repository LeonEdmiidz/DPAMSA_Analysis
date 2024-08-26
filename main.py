# Removed the lines of code importing the unknown datasets
import sys
import os
from tqdm import tqdm
import config
from env import Environment
from dqn import DQN
# The Biopython module is used to load in fasta file datasets
from Bio import SeqIO
import torch
# The time module is used to record the run time for DPAMSA
import time

def main():
    # Included to ensure that the fasta file is being inputted when running the script
    if len(sys.argv) < 2:
        print("Usage: python main.py <fasta_file> [<num_datasets>]")
        return

    # This line ensures that a GPU node is being used if available
    config.device_name = "cuda:0" if torch.cuda.is_available() else "cpu"
    config.device = torch.device(config.device_name)
    # The fasta file provided in the command line is the input dataset to be aligned
    fasta_file = sys.argv[1]

    # Load sequences from the fasta file using the BioPython tools
    sequences = {record.id: str(record.seq) for record in SeqIO.parse(fasta_file, "fasta")}

    # This if-then statement ensure that the correct training function is used
    # For this project, the multi_train function is not used
    if len(sys.argv) > 2:
        num_datasets = int(sys.argv[2])
        multi_train(sequences, num_datasets)
    else:
        # Train on single dataset
        train(sequences)

def output_parameters():
    print("Gap penalty: {}".format(config.GAP_PENALTY))
    print("Mismatch penalty: {}".format(config.MISMATCH_PENALTY))
    print("Match reward: {}".format(config.MATCH_REWARD))
    print("Episode: {}".format(config.max_episode))
    print("Batch size: {}".format(config.batch_size))
    print("Replay memory size: {}".format(config.replay_memory_size))
    print("Alpha: {}".format(config.alpha))
    print("Epsilon: {}".format(config.epsilon))
    print("Gamma: {}".format(config.gamma))
    print("Delta: {}".format(config.delta))
    print("Decrement iteration: {}".format(config.decrement_iteration))
    print("Update iteration: {}".format(config.update_iteration))
    print("Device: {}".format(config.device_name))

# Although not used in this project, this function was altered to ensure that the fasta files are loaded in properly
def multi_train(sequences, num_datasets):
    output_parameters()
    print("Dataset number: {}".format(num_datasets))

    report_file_name = os.path.join(config.report_path, "multi_train.rpt")

    with open(report_file_name, 'w') as _:
        _.truncate()

    # Split sequences into datasets
    seq_per_dataset = len(sequences) // num_datasets
    datasets = [sequences[i:i + seq_per_dataset] for i in range(0, len(sequences), seq_per_dataset)]

    # Train on each dataset
    for index, seqs in enumerate(datasets):
        env = Environment(seqs)
        agent = DQN(env.action_number, env.row, env.max_len, env.max_len * env.max_reward)
        p = tqdm(range(config.max_episode))
        p.set_description(f"Dataset {index + 1}")

        for _ in p:
            state = env.reset()
            while True:
                action = agent.select(state)
                reward, next_state, done = env.step(action)
                agent.replay_memory.push((state, next_state, action, reward, done))
                agent.update()
                if done == 0:
                    break
                state = next_state
            agent.update_epsilon()

        state = env.reset()

        while True:
            action = agent.predict(state)
            _, next_state, done = env.step(action)
            state = next_state
            if 0 == done:
                break

        env.padding()
        report = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n\n".format("NO: {}".format(name),
                                                         "AL: {}".format(len(env.aligned[0])),
                                                         "SP: {}".format(env.calc_score()),
                                                         "EM: {}".format(env.calc_exact_matched()),
                                                         "CS: {}".format(
                                                             env.calc_exact_matched() / len(env.aligned[0])),
                                                         "QTY: {}".format(len(env.aligned)),
                                                         "#\n{}".format(env.get_alignment()))

        with open(os.path.join(config.report_path, "{}.rpt".format(tag)), 'a+') as report_file:
            report_file.write(report)


def train(sequences):
    output_parameters()

# Commented out the lines below as they relate to the unspecified data format.
#    assert hasattr(dataset, "dataset_{}".format(index)), "No such data called {}".format("dataset_{}".format(index))
#    data = getattr(dataset, "dataset_{}".format(index))
#    print("{}: dataset_{}: {}".format(dataset.file_name, index, data))
    # Set the start time to record the run time
    train_start_time = time.monotonic()
    # These print statements confirm the sequences that are being aligned
    print(f"Training on {len(sequences)} sequences:")
    for key in sequences:  # Iterate over keys and values
        print(f"Sequence {key}")
    env = Environment(list(sequences.values()))
    agent = DQN(env.action_number, env.row, env.max_len, env.max_len * env.max_reward)
    p = tqdm(range(config.max_episode))

    for _ in p:
        state = env.reset()
        while True:
            action = agent.select(state)
            reward, next_state, done = env.step(action)
            agent.replay_memory.push((state, next_state, action, reward, done))
            agent.update()
            if done == 0:
                break
            state = next_state
        agent.update_epsilon()
    # The end time for training is recorded for run time calculation
    train_end_time = time.monotonic()
    # Print statement for checkpoint confirmation
    print("Training Complete")
    # Run time calculation
    train_time = train_end_time - train_start_time
    # Print training time formatted to 2 decimal places
    print(f"Training time: {train_time:.2f} seconds")

    # Predicting the alignment based off the training
    # Record start time for run time calculation
    predict_start_time = time.monotonic()
    state = env.reset()
    while True:
        action = agent.predict(state)
        _, next_state, done = env.step(action)
        state = next_state
        if 0 == done:
            break
    # Record end time for run time calculation
    predict_end_time = time.monotonic()
    # Print statement for checkpoint confirmation
    print("Prediction Complete")
    # Calculate the prediction time
    predict_time = predict_end_time - predict_start_time
    # Print predicting time formatted to 2 decimal places
    print(f"Predict time: {predict_time:.2f} seconds")

    env.padding()
#    print("**********dataset: {} **********\n".format(data))
    print("total length : {}".format(len(env.aligned[0])))
    print("sp score     : {}".format(env.calc_score()))
    print("exact matched: {}".format(env.calc_exact_matched()))
    print("column score : {}".format(env.calc_exact_matched() / len(env.aligned[0])))
    print("alignment: \n{}".format(env.get_alignment()))
    print("********************************\n")


if __name__ == "__main__":
    main()
