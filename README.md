<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![CI][ci-shield]][ci-url]
[![MIT License][license-shield]][license-url]
[![Python][python-shield]][python-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">EBNF Compiler</h3>

  <p align="center">
    A Python tool for parsing and analyzing Extended Backus-Naur Form (EBNF) grammars - with a clean CLI, AST output, and symbol analysis.
    <br />
    <a href="https://github.com/swaiku/EBNF-Compiler"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#usage">View Demo</a>
    &middot;
    <a href="https://github.com/swaiku/EBNF-Compiler/issues/new?labels=bug">Report Bug</a>
    &middot;
    <a href="https://github.com/swaiku/EBNF-Compiler/issues/new?labels=enhancement">Request Feature</a>
  </p>
</div>

---

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#getting-started">Getting Started</a>
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

---

## About The Project

**EBNF Compiler** is a command-line tool that parses [Extended Backus-Naur Form (EBNF)](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form) grammar files. It performs lexical scanning, recursive-descent parsing, and builds a full Abstract Syntax Tree (AST) from EBNF source files.

Key features:
- **Lexical scanner** with support for nested comments `(* ... (* ... *) ... *)`
- **Recursive-descent parser** that validates EBNF syntax
- **AST construction** with rich terminal output
- **Symbol analysis** - identifies terminals and non-terminals in a grammar
- **Clean CLI** powered by [Typer](https://typer.tiangolo.com/) and [Rich](https://github.com/Textualize/rich)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [![Python][python-shield]][python-url]
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://github.com/Textualize/rich) - Terminal formatting
- [Loguru](https://github.com/Delgan/loguru) - Logging
- [uv](https://github.com/astral-sh/uv) - Package manager & build tool
- [Ruff](https://github.com/astral-sh/ruff) - Linter & formatter
- [Pytest](https://pytest.org/) - Testing

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Getting Started

### Prerequisites

- Python **3.11+**
- [`uv`](https://github.com/astral-sh/uv) package manager

#### Linux / MacOS
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation

1. Clone the repository

   ```sh
   git clone https://github.com/swaiku/EBNF-Compiler.git
   cd EBNF-Compiler
   ```

2. Install dependencies with `uv`

   ```sh
   uv sync
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Usage

The CLI entry point is `ebnf-compiler`.

```sh
ebnf-compiler <source.ebnf> [OPTIONS]
```

### Options

| Flag | Description |
|------|-------------|
| `--show-tree` | Print the full Abstract Syntax Tree |
| `--show-symbols` | List terminals and non-terminals |
| `--debug` | Enable debug logging |

### Examples

**Parse a grammar file:**

```sh
ebnf-compiler examples/basic.ebnf
```

**Show the AST:**

```sh
ebnf-compiler examples/oberon0.ebnf --show-tree
```

**Analyze grammar symbols:**

```sh
ebnf-compiler examples/ebnf.ebnf --show-symbols
```

### Example EBNF Grammar (`examples/basic.ebnf`)

```ebnf
ident  = letter { letter | digit }.
number = digit { digit }.
digit  = "0" | "1" | "2" | "3".
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Roadmap

- [x] Lexical scanner with nested comment support
- [x] Recursive-descent parser
- [x] AST construction and display
- [x] Symbol analysis (terminals / non-terminals)
- [x] Rich CLI output
- [ ] Semantic analysis (undefined/unused symbols)
- [ ] Code generation backend
- [ ] Support for additional grammar formats

See the [open issues](https://github.com/swaiku/EBNF-Compiler/issues) for a full list of proposed features and known issues.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Contributing

Contributions are welcome and greatly appreciated.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## License

Distributed under the **MIT** license. See [`LICENSE`](LICENSE) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Contact

**Jérémy Prin** - [@swaiku](https://github.com/swaiku)

Project link: [https://github.com/swaiku/EBNF-Compiler](https://github.com/swaiku/EBNF-Compiler)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Acknowledgments

- [othneildrew/Best-README-Template](https://github.com/othneildrew/Best-README-Template)
- [EBNF - Wikipedia](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form)
- [Img Shields](https://shields.io)
- [Choose an Open Source License](https://choosealicense.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- MARKDOWN LINKS & IMAGES -->
[ci-shield]: https://img.shields.io/github/actions/workflow/status/swaiku/EBNF-Compiler/ci.yml?branch=main&style=for-the-badge&label=CI
[ci-url]: https://github.com/swaiku/EBNF-Compiler/actions/workflows/ci.yml
[license-shield]: https://img.shields.io/badge/license-MIT-green?style=for-the-badge
[license-url]: https://github.com/swaiku/EBNF-Compiler/blob/main/LICENSE
[python-shield]: https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org/
