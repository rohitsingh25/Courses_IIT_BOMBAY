import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle as pkl


class NaiveBayes:
    def fit(self, X, y):
        self.classes = np.unique(y)
        self.priors = {}
        self.gaussian = {}
        self.bernoulli = {}
        self.laplace = {}
        self.exponential = {}
        self.multinomial = {}

        for c in self.classes:
            X_c = X[y == c]
            self.priors[str(c)] = len(X_c) / len(X)
            self.gaussian[str(c)] = {
                "mean": np.mean(X_c, axis=0),
                "variance": np.var(X_c, axis=0)
            }
            p_x3 = np.mean(X_c[:, 2])
            p_x4 = np.mean(X_c[:, 3])
            self.bernoulli[str(c)] = [p_x3, p_x4]
            mu_x5 = np.mean(X_c[:, 4])
            mu_x6 = np.mean(X_c[:, 5])
            b_x5_x6 = np.mean(np.abs(X_c[:, 4] - mu_x5))
            self.laplace[str(c)] = [mu_x5, mu_x6, b_x5_x6]
            lambda_x7 = 1 / np.mean(X_c[:, 6])
            lambda_x8 = 1 / np.mean(X_c[:, 7])
            self.exponential[str(c)] = [lambda_x7, lambda_x8]
            p_x9 = np.mean(X_c[:, 8])
            p_x10 = np.mean(X_c[:, 9])
            self.multinomial[str(c)] = [[p_x9, 1 - p_x9], [p_x10, 1 - p_x10]]
        """End of your code."""
        # print(self.gaussian)
        # print(self.bernoulli)
        # print(self.laplace)
        # print(self.exponential)
        # print(self.multinomial)

    def predict(self, X):
        predictions = []
        for x in X:
            posteriors = []

            for c in self.classes:
                posterior = np.log(self.priors[str(c)])
                gaussian_params = self.gaussian[str(c)]
                posterior -= 0.5 * np.sum(np.log(2 * np.pi * gaussian_params["variance"]))
                posterior -= 0.5 * np.sum(((x - gaussian_params["mean"]) ** 2) / gaussian_params["variance"])
                p_x3, p_x4 = self.bernoulli[str(c)]
                posterior += np.sum(x[2] * np.log(p_x3) + (1 - x[2]) * np.log(1 - p_x3))
                posterior += np.sum(x[3] * np.log(p_x4) + (1 - x[3]) * np.log(1 - p_x4))
                laplace_params = self.laplace[str(c)]
                posterior -= np.sum(np.abs(x[4:6] - laplace_params[:2]) / laplace_params[2])
                exponential_params = self.exponential[str(c)]
                posterior += np.sum(-exponential_params[0] * x[6:8])
                multinomial_params = self.multinomial[str(c)]
                epsilon = 1e-10  
                posterior += np.sum(x[8:] * np.log(np.maximum(multinomial_params, epsilon)))
                posteriors.append(posterior)  
            if any(np.isfinite(posteriors)):
                predicted_class = self.classes[np.argmax(posteriors)]
            else:
                predicted_class = 0

            predictions.append(predicted_class)

        return np.array(predictions)
    


    def getParams(self):
        """
        Return your calculated priors and parameters for all the classes in the form of dictionary that will be used for evaluation
        Please don't change the dictionary names
        Here is what the output would look like:
        priors = {"0":0.2,"1":0.3,"2":0.5}
        gaussian = {"0":[mean_x1,mean_x2,var_x1,var_x2],"1":[mean_x1,mean_x2,var_x1,var_x2],"2":[mean_x1,mean_x2,var_x1,var_x2]}
        bernoulli = {"0":[p_x3,p_x4],"1":[p_x3,p_x4],"2":[p_x3,p_x4]}
        laplace = {"0":[mu_x5,mu_x6,b_x5,b_x6],"1":[mu_x5,mu_x6,b_x5,b_x6],"2":[mu_x5,mu_x6,b_x5,b_x6]}
        exponential = {"0":[lambda_x7,lambda_x8],"1":[lambda_x7,lambda_x8],"2":[lambda_x7,lambda_x8]}
        multinomial = {"0":[[p0_x9,...,p4_x9],[p0_x10,...,p7_x10]],"1":[[p0_x9,...,p4_x9],[p0_x10,...,p7_x10]],"2":[[p0_x9,...,p4_x9],[p0_x10,...,p7_x10]]}
        """
        priors = {}
        guassian = {}
        bernoulli = {}
        laplace = {}
        exponential = {}
        multinomial = {}

        """Start your code"""
        return [self.priors,self.gaussian,self.bernoulli,self.laplace,self.exponential,self.multinomial]
        """End your code"""
        # return (priors, guassian, bernoulli, laplace, exponential, multinomial)        


def save_model(model,filename="model.pkl"):
    """

    You are not required to modify this part of the code.

    """
    file = open("model.pkl","wb")
    pkl.dump(model,file)
    file.close()

def load_model(filename="model.pkl"):
    """

    You are not required to modify this part of the code.

    """
    file = open(filename,"rb")
    model = pkl.load(file)
    file.close()
    return model

def visualise(data_points,labels):
    """
    datapoints: np.array of shape (n,2)
    labels: np.array of shape (n,)
    """

    plt.figure(figsize=(8, 6))
    plt.scatter(data_points[:, 0], data_points[:, 1], c=labels, cmap='viridis')
    plt.colorbar()
    plt.title('Generated 2D Data from 5 Gaussian Distributions')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.show()


def net_f1score(predictions, true_labels):
    def precision(predictions, true_labels, label):
        true_positives = np.sum((predictions == label) & (true_labels == label))
        false_positives = np.sum((predictions == label) & (true_labels != label))
        denominator = true_positives + false_positives
        if denominator == 0:
            return 0  # Handle division by zero
        return true_positives / denominator
 
    def recall(predictions, true_labels, label):
        true_positives = np.sum((predictions == label) & (true_labels == label))
        false_negatives = np.sum((predictions != label) & (true_labels == label))
        denominator = true_positives + false_negatives
        if denominator == 0:
            return 0  # Handle division by zero
        return true_positives / denominator

    def f1score(predictions, true_labels, label):
        prec = precision(predictions, true_labels, label)
        rec = recall(predictions, true_labels, label)
        if prec + rec == 0:
            return 0  # Handle division by zero
    
        f1 = 2 * (prec * rec) / (prec + rec)
        return f1
    f1s = []
    for label in np.unique(true_labels):
        f1s.append(f1score(predictions, true_labels, label))
    return f1s

def accuracy(predictions,true_labels):
    """

    You are not required to modify this part of the code.

    """
    return np.sum(predictions==true_labels)/predictions.size



if __name__ == "__main__":
    """

    You are not required to modify this part of the code.

    """

    # Load the data
    train_dataset = pd.read_csv('./data/train_dataset.csv',index_col=0).to_numpy()
    validation_dataset = pd.read_csv('./data/validation_dataset.csv',index_col=0).to_numpy()

    # Extract the data
    train_datapoints = train_dataset[:,:-1]
    train_labels = train_dataset[:, -1]
    validation_datapoints = validation_dataset[:, 0:-1]
    validation_labels = validation_dataset[:, -1]
    model = NaiveBayes()
    model.fit(train_datapoints, train_labels)

    # Make predictions
    train_predictions = model.predict(train_datapoints)
    validation_predictions = model.predict(validation_datapoints)

    # Calculate the accuracy
    train_accuracy = accuracy(train_predictions, train_labels)
    validation_accuracy = accuracy(validation_predictions, validation_labels)

    # Calculate the f1 score
    train_f1score = net_f1score(train_predictions, train_labels)
    validation_f1score = net_f1score(validation_predictions, validation_labels)

    # Print the results
    print('Training Accuracy: ', train_accuracy)
    print('Validation Accuracy: ', validation_accuracy)
    print('Training F1 Score: ', train_f1score)
    print('Validation F1 Score: ', validation_f1score)

    # Save the model
    save_model(model)
