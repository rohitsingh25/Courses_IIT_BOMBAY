import numpy as np
import matplotlib.pyplot as plt
class LogisticRegression:
    def __init__(self):
        """
        Initialize `self.weights` properly. 
        Recall that for binary classification we only need 1 set of weights (hence `num_classes=1`).
        We have given the default zero intialization with bias term (hence the `d+1`).
        You are free to experiment with various other initializations including random initialization.
        Make sure to mention your initialization strategy in your report for this task.
        """
        self.num_classes = 1 # single set of weights needed
        self.d = 2 # input space is 2D. easier to visualize
        self.weights = np.zeros((self.d+1, self.num_classes))
    
    def preprocess(self, input_x):
        """
        Preprocess the input any way you seem fit.
        """
        return input_x

    def sigmoid(self, x):
        """
        Implement a sigmoid function if you need it. Ignore otherwise.

        """
        f=1/(1+np.exp(-x))
        return f
        

    def calculate_loss(self, input_x, input_y):
        """
        Arguments:
        input_x -- NumPy array with shape (N, self.d) where N = total number of samples
        input_y -- NumPy array with shape (N,)
        Returns: a single scalar value corresponding to the loss.
        """
        input_x = self.preprocess(input_x)
        new_column=np.ones(input_x.shape[0]).reshape(input_x.shape[0],1)
        # print(input_x.shape)
        # print(input_x)
        input_y = input_y.reshape((-1, 1)).T
        input_x=np.append(new_column,input_x,axis=1)
        s=np.dot( input_x,self.weights)+self.weights[0]
        c=self.sigmoid(s)
        # loss= -np.mean(input_y*np.log(c) + (1-input_y)*np.log(1-c))
        # print(input_y.shape, c.shape)
        loss= np.mean((input_y * np.log(c)) + ((1-input_y) * np.log(1-c)))
        # 1 print(loss, "loss function")
        # print("**********************",loss)
        # print("loss shape",loss)
        # 2 
        loss = -(loss)/2
        return loss.item()

    def calculate_gradient(self, input_x, input_y):
        """
        Arguments:
        input_x -- NumPy array with shape (N, self.d) where N = total number of samples
        input_y -- NumPy array with shape (N,)
        Returns: the gradient of loss function wrt weights.
        Ensure that gradient.shape == self.weights.shape.
        """
        input_x=self.preprocess(input_x) 
        new_column=np.ones(input_x.shape[0]).reshape(input_x.shape[0],1)
        input_x=np.append(input_x,new_column,axis=1)
        b=np.dot( input_x,self.weights)+self.weights[0]
        s=self.sigmoid(b)
        i=np.dot(input_x.T,(s-input_y.reshape(-1,1)))/len(input_y)
        # 3 print(self.weights)
        return i

    def update_weights(self, grad, learning_rate, momentum):
        """
        Arguments:
        grad -- NumPy array with same shape as `self.weights`
        learning_rate -- scalar
        momentum -- scalar
        Returns: nothing
        The function should update `self.weights` with the help of `grad`, `learning_rate` and `momentum`
        """
        #self.weights=np.append(self.weights+[1])
        # print("grad shape")
        # print(grad.shape)
        # print("weights shape")
        # print(self.weights)
        # self.weights-=momentum*learning_rate*grad
        self.weights -= learning_rate * grad
        self.weights[0]-=learning_rate*np.sum(grad)/len(grad)
        


    def get_prediction(self, input_x):
        """
        Arguments:
        input_x -- NumPy array with shape (N, self.d) where N = total number of samples
        Returns: a NumPy array with shape (N,) 
        The returned array must be the list of predicted class labels for every input in `input_x`
        """
        input_x=self.preprocess(input_x)
        new_column=np.ones(input_x.shape[0]).reshape(input_x.shape[0],1)
        input_x=np.append(input_x,new_column,axis=1)
        b=np.dot( input_x,self.weights)+self.weights[0]
        s=self.sigmoid(b)
        p=(s>=0.5).astype(int)
        # print("Printing ppppppppppppppppp")
        # print(p.T)
        return p.T

class LinearClassifier:
    def __init__(self):
        """
        Initialize `self.weights` properly. 
        We have given the default zero intialization with bias term (hence the `d+1`).
        You are free to experiment with various other initializations including random initialization.
        Make sure to mention your initialization strategy in your report for this task.
        """
        self.num_classes = 3 # 3 classes
        self.d = 4 # 4 dimensional features
        self.weights = np.zeros((self.d+1, self.num_classes))
        self.v = 0
    def preprocess(self, train_x):
        """
        Preprocess the input any way you seem fit.
        """
        return train_x

    def sigmoid(self, x):
        """
        Implement a sigmoid function if you need it. Ignore otherwise.
        """
        f=1/(1+np.exp(-x))
        return f

    def calculate_loss(self, input_x, input_y):
        """
        Arguments:
        input_x -- NumPy array with shape (N, self.d) where N = total number of samples
        input_y -- NumPy array with shape (N,)
        Returns: a single scalar value corresponding to the loss.
        """
        i= input_x.shape[0]
        input_x = np.concatenate((input_x, np.ones((i, 1))), axis=1)  
        output = np.dot(input_x, self.weights)  
        pred = self.sigmoid(output)  
        ls= np.dot(input_y, np.log(pred)) - np.dot((1-input_y), np.log(1-pred))
        total_loss = np.sum(ls) / i
        #  4
        total_loss = -(total_loss) / 3
        return total_loss
    

    def calculate_gradient(self, input_x, input_y):
        """
        Arguments:
        input_x -- NumPy array with shape (N, self.d) where N = total number of samples
        input_y -- NumPy array with shape (N,)
        Returns: the gradient of loss function wrt weights.
        Ensure that gradient.shape == self.weights.shape.
        """
        i = input_x.shape[0]
        input_x = np.concatenate((input_x, np.ones((i, 1))), axis=1) 
        output= np.dot(input_x, self.weights)  
        pred = self.sigmoid(output)  
        r = np.zeros_like(self.weights)
        m = np.zeros_like(pred)
        m[np.arange(i), input_y] = 1
        r = np.dot(input_x.T, pred - m) / i
        return r

    def update_weights(self, grad, learning_rate, momentum):
        """
        Arguments:
        grad -- NumPy array with same shape as `self.weights`
        learning_rate -- scalar
        momentum -- scalar
        Returns: nothing
        The function should update `self.weights` with the help of `grad`, `learning_rate` and `momentum`
        """
        # self.v = 0
        self.v=momentum * self.v - learning_rate * grad
        self.weights +=  self.v
        

    def get_prediction(self, input_x):
        """
        Arguments:
        input_x -- NumPy array with shape (N, self.d) where N = total number of samples
        Returns: a NumPy array with shape (N,) 
        The returned array must be the list of predicted class labels for every input in `input_x`
        """
        i = input_x.shape[0]
        input_x = np.concatenate((input_x, np.ones((i, 1))), axis=1)  
        output = np.dot(input_x, self.weights)  
        pred = self.sigmoid(output)          
        pred_l = np.argmax(pred, axis=1)
        return pred_l
