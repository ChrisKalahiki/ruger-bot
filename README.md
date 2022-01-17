<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ChrisKalahiki/ruger-bot">
    <img src="assets/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Ruger Bot</h3>

  <p align="center">
    A Discord bot for use in my personal server.
    <br />
    <a href="https://github.com/ChrisKalahiki/ruger-bot"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ChrisKalahiki/ruger-bot">View Demo</a>
    ·
    <a href="https://github.com/ChrisKalahiki/ruger-bot/issues">Report Bug</a>
    ·
    <a href="https://github.com/ChrisKalahiki/ruger-bot/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Python](https://www.python.org/)
* [Discord.py](https://discordpy.readthedocs.io/en/stable/)
* [Spotipy](https://spotipy.readthedocs.io/en/2.19.0/)
* [NLTK](https://www.nltk.org/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This project has a few pre-requisites before you can get up and running. They are as follows:
1. [Docker](https://www.docker.com/)
2. [Python 3.6+](https://www.python.org/downloads/)
3. [Discord API Token](https://discord.com/developers/applications)
4. [Spotify API Key](https://developer.spotify.com/dashboard/applications)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/ChrisKalahiki/ruger-bot.git
   ```
2. Create a JSON file called pass.json with the following contents:
  ```{
      "spotify":{
          "clientID":"yourClientID",
          "clientSecret":"yourClientSecret"",
          "redirectURI":"yourRedirectURI"
      },
      "discord":"yourDiscordToken"
  }```
3. Create a new log file called `discord.log` in the logs directory
4. Build the Docker image
   ```
   docker build -t ruger-bot .
   ```
5. Run the Docker image
    ```
    docker run -dp 3000:3000 ruger-bot
    ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [] Feature 1
- [] Feature 2
- [] Feature 3
    - [] Nested Feature

See the [open issues](https://github.com/ChrisKalahiki/ruger-bot/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@ChrisKalahiki](https://twitter.com/@ChrisKalahiki) - chris.kalahiki@gmail.com

Project Link: [https://github.com/ChrisKalahiki/ruger-bot](https://github.com/ChrisKalahiki/ruger-bot)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Chris Kalahiki](https://www.chriskalahiki.info/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ChrisKalahiki/ruger-bot.svg?style=for-the-badge
[contributors-url]: https://github.com/ChrisKalahiki/ruger-bot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ChrisKalahiki/ruger-bot.svg?style=for-the-badge
[forks-url]: https://github.com/ChrisKalahiki/ruger-bot/network/members
[stars-shield]: https://img.shields.io/github/stars/ChrisKalahiki/ruger-bot.svg?style=for-the-badge
[stars-url]: https://github.com/ChrisKalahiki/ruger-bot/stargazers
[issues-shield]: https://img.shields.io/github/issues/ChrisKalahiki/ruger-bot.svg?style=for-the-badge
[issues-url]: https://github.com/ChrisKalahiki/ruger-bot/issues
[license-shield]: https://img.shields.io/github/license/ChrisKalahiki/ruger-bot.svg?style=for-the-badge
[license-url]: https://github.com/ChrisKalahiki/ruger-bot/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/chriskalahiki
[product-screenshot]: images/screenshot.png
