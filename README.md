# eMigrator

_Tool designed to massively migrate email accounts between multiple email servers._

## Getting Started 🚀

### Prerequisites 📋

_You will need to create a file called "migrationData.csv" where you can enter the data in the format indicated below._

| originServer       | originServerPort | originAccount      | originAccountPasswd | destinationServer  | destinationServerPort | destinationAccount | destinationAccountPasswd |
|--------------------|------------------|--------------------|---------------------|--------------------|-----------------------|--------------------|--------------------------|
| mail.oldserver.com | 143              | user@oldserver.com | unsafepasswd1234    | mail.newserver.com | 993                   | user@newserver.com | SuperSafePasswd1324%     |


## Built With 🛠️

* [Python 3.9](https://www.python.org/) - Programming language in which the tool is written.

## Versions 📌

* **V. 1 _(08/01/2021)_ --->** The tool generates a folder with a timestamp by name and creates the subdirectories of each email account one by one, filling them with the downloaded emails, and then uploading them to the new server.

* **V. 2 _(Working on it...)_ --->** At the end of the copy, the tool compresses the root directory, thus leaving a backup copy for the future. Furthermore, the tool is already capable of creating email accounts on a target Plesk server.

## Authors ✒️

* **Jorge B. [[Noob In The Net](https://github.com/noobinthenet)]** - *Full Development*

## License 📄

This project is licensed under the "GNU Affero General Public License v3.0", see the [LICENSE.md](LICENSE.md) file for more details.

## Gratitude 🎁

* [jesusamoros](https://github.com/jesusamoros) - Helped with testing in a real environment and with the implementation of the automatic mail creation function in Plesk.

---
⌨️ con ❤️ por [Noob In The Net](https://github.com/Villanuevand) 😊
