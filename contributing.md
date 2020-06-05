# Contributing

## Requirements

Requirements for contributing to this project:
1. Being at ease with programming (preferably in Python) and version control (Git).

Strong nice to have (but not required):
1. Practical understanding of time/space complexity, algorithms and data structures.

## Process

If you want to contribute to the project, here's the procedure that you should follow. You can contribute if you have some idea how this library could be improved, but also if you don't have any ideas.

If you have any questions, you can ask them on "Discussions" page or "Issues" page in this repository or you can email me on damiancz@mailfence.com.

The below procedure is a standard software development cycle, you don't have to read this, if you're familiar with it.

1. Go to the "Issues" page of this repository (<https://github.com/damc/simple-algs/issues>). On the "Issues" page you have all tasks that we have to do.
2. Choose an issue (task) that you want to work on. If you want to work on something that is not there (some idea of how this library could be improved), then add a new issue. When choosing issue to work on take into account:
    1. priority (it's in the description of the issue);
    2. estimated time (to finish the task);
    3. don't work on an issue that someone is already assigned to.

When creating a new issue, please include the following things in the description:
    1. What needs to be done.
    2. Priority (possible priorities: urgent, super required, required, nice to have, a bit nice to have).
    3. Estimated time (that it will take to finish the issue).
    4. Which issues (tasks) needs to be done before that issue, if there is anything blocking the issue that you are adding.

Sometimes you can add a task without this information and add this information later.

3. Assign yourself to the issue that you want to work on.
4. Create a new branch.
5. Do the issue (task) on the new branch. Follow the PEP 8 style guide for Python code. Write the docstrings in markdown so that it's possible to automatically generate the website documentation. Take docstrings from <https://github.com/keras-team/keras/blob/master/keras/layers/convolutional.py>(Keras) library as a pattern on how to write docstrings in this project.
6. Test your work (it's recommended to test it using unit testing).
7. Commit your work on your branch and push your branch to the main repository.
8. Create a pull request (from your branch to "master" branch). You can do this by going to "Pull requests" ( <https://github.com/damc/simple-algs/pulls> ). Also, after you push your branch, Git should give you a link to create a new pull request in response to your push.
9. Make sure that the build is ok and all checks are ok (there are automatic checks if all unit tests pass and code quality checks using Lint). If something is wrong, then fix it, commit and push again.
10. Wait until someone approves your pull request. If there any comments on what you could improve, then make the suggested improvements (if the suggestions are good, in your opinion) or debate on why they are not a good idea (if the suggestions are bad, in your opinion).
11. Merge it. Click "Squash and merge" so that all commits from that issue are squashed into one commit. Make sure that the issue number is in the name of the squashed commit (the number should be prefixed with "#").
12. Job done.

Repeat the above process as long as you want to contribute to the project.

# Other ways

Other ways how you can contribute:
1. Add issue proposing new improvement/feature/challenge on the "Issues" page.
2. Go to "Pull requests" and review the pull requests.
