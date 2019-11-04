# Contribution Guidelines

Thanks for investing the time to contribute!

The CytoData 2019 Hackathon focused on developing solutions to classify mechanism-of-action (MOA) phenotypes in single cells.
We used images and image-based profiles to determine MOA.

The following document contains a set of guidelines for how to best contribute to the analytical code base.

## Open Science

We will pursue this project using [Open Science](https://en.wikipedia.org/wiki/Open_science).
Be aware that any code added to this repository will be posted under a [CC-BY-4.0 International License](LICENSE.md).

## Pull Request Model

We will be operating under a pull request model.
Please refer to [this guide](https://gist.github.com/Chaser324/ce0505fbed06b947d962) explaining how forking and branching works under such a model.

The best pull requests consist of:

1. Adding or updating a single feature
2. Clear and concise description of the change
3. A confirmation that the entire analysis still runs
4. Fully ["linted"](https://en.wikipedia.org/wiki/Lint_%28software%29) code.

A pull request template is provided in the [`PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md).

## Code Review

The only way code can be accepted and merged into the repository is after a thorough code review by _one_ other member familiar with
the code base.

## Style

Our goal is to have readable, concise, and working code.

We follow the [PEP8](https://www.python.org/dev/peps/pep-0008/) style guide for python and [Google's style guide for R](https://google.github.io/styleguide/Rguide.xml).

Code can be quickly made to follow style guides by a linter (e.g. [Flake8](https://atom.io/packages/linter-flake8)) or by [`black`](https://pypi.org/project/black/).
Please make sure code style is updated prior to code review.

Do not hesitate to ask for help reviewing code and or creating a pull request!

## Code of Conduct

This is described in the [`CODE_OF_CONDUCT.md`](.github/CODE_OF_CONDUCT.md) document.
