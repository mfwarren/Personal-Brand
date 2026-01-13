# Learning AI Algorithms

One of my goals for the year is to get deeper into learning the new generation of AI algorithms and practice getting good at applying those to real problems. AI has been one of those areas that always fascinated me, and then I took the AI course at university and learned that it just wasn't as difficult or as interesting once the covers had been lifted on the mystique of it.

There are many approaches to algorithms that can be classified as AI. If you consider that AI is the ability of a program to be given a dataset and then answer questions outside that dataset then something as simple as a linear regression is considered an AI.

```python
#!/usr/bin/env python3
import random

def linear_regression(x, y):
    length = len(x)
    sum_x = sum(x)
    sum_y = sum(y)

    # Σx**2 and Σxy
    sum_x_squared = sum(map(lambda a: a*a, x))
    sum_of_products = sum([x[i] * y[i] for i in range(length)])

    a = (sum_of_products - (sum_x * sum_y) / length) / (sum_x_squared - ((sum_x**2) / length))
    b = (sum_y - a * sum_x) / length
    return a, b  # y = ax + b

if __name__ == '__main__':
    simple_data = [[0, 10], [0, 10]]  # slope=1, intercept=0
    print(linear_regression(*simple_data))

    random_data = [list(range(1000)), [random.triangular(20, 99, 70) for i in range(1000)]]
    # should be slope ~=0 intercept ~= 70
    print(linear_regression(*random_data))
```

In a real world example this would be expanded into an N dimensional regression where each dimension is an attribute. As the data gets bigger and bigger, regressions need more advanced techniques to compute things efficiently. But ultimately it never feels like you're doing something emergent, you're just doing math.

Decision trees are another popular form of AI algorithm. In the most basic form this is just a binary tree of questions, to answer a question like "do I have cancer?" you start at the top of the tree and answer yes or no questions at each node until you reach the leaf which should provide the answer. Again these get more advanced as they are applied to more difficult use cases but never really get to the point where they feel like an intelligence.

Neural networks and the new research in deep learning approaches are by far the most interesting, and yet they are also still nowhere near a state of general intelligence. A neuron in a neural network is a simple program that takes input, modifies it and sends that as output and accepts feedback to re-inforce positive modifications. These neurons are then connected into vast networks, usually in layers.

The breakthrough in deep learning is that we can provide re-inforcement at different layers in the network for successively more specific things and get better results. Applied to a data set these can do remarkably well at things like identifying faces in a photo.

There is a bit of artistry required to apply these to a real world problem. Given data and a problem to answer from it, which type of algorithm do you use, how does the data need to be cleaned up or re-factored, how will you train and verify your AI algorithm afterwards? There's enough options there that just choosing a path to go on is often the most difficult task.

The whole AI space still is at its infancy and really needs a genius to come in and shake up everything. All the current approaches are narrow in scope and a breakthrough is required to find a path that will lead to a strong general AI.
