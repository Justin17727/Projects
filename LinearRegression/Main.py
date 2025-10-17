import numpy as np


class LinearRegression:
    def __init__(self):
        self.m = None  # slope
        self.b = None  # intercept

    def fit(self, x: list[int], y: list[int]):
        x_mean = np.mean(x)
        y_mean = np.mean(y)

        x_centered = x - x_mean
        y_centered = y - y_mean

        numerator = np.multiply(x_centered, y_centered)
        denominator = np.square(x_centered)

        self.m = sum(numerator) / sum(denominator)

        self.b = y_mean - (self.m * x_mean)

        print(self.m)
        print(self.b)

    def predict(self, x: list[float]) -> list[float]:
        y = np.add(np.multiply(x, self.m), self.b)
        return y


print(np.multiply([1, 2, 3], 2) + 8)


X = [1, 2, 2.5, 3, 3.5, 4, 4.5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5]
Y = [10, 16, 20, 25, 28, 32, 35, 44, 48, 52, 55, 60, 65, 70, 75, 80]
model = LinearRegression()
model.fit(X, Y)
print(model.predict([10, 12]))
