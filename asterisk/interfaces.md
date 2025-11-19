# An Interface for Communications Applications

<img width="516" height="298" alt="AMI-ARI-AGI" src="https://github.com/user-attachments/assets/0032d3f4-cae4-4283-85ca-f6e294af683d" />


## [Enter AMI and AGI](https://docs.asterisk.org/Configuration/Interfaces/Asterisk-REST-Interface-ARI/#enter-ami-and-agi)
Not long into the project, two application programming interfaces (APIs) were added to Asterisk: 

-   the Asterisk Gateway Interface (AGI) and
-   the Asterisk Manager Interface (AMI).

These interfaces have distinct purposes:

### AGI

AGI is analogous to CGI in Apache. AGI provides an interface between the Asterisk dialplan and an external program that wants to manipulate a channel in the dialplan.

In general, the interface is synchronous - actions taken on a channel from an AGI block **and do not return until the action is completed**.

> [!NOTE]
> Using AGI, remote dialplan execution could be enabled, which allowed developers to integrate Asterisk with PHP, Python, Java, and other applications.

### AMI

AMI provides a mechanism to control where channels execute in the dialplan. Unlike AGI, AMI is an asynchronous, event driven interface.

For the most part, **AMI does not provide mechanisms to control channel execution** - rather, it provides information about **the state of the channels** and controls about where the channels are executing.

> [!NOTE]
> Using AMI, the state of Asterisk could be displayed, calls initiated, and the location of channels controlled.


Both of these interfaces are powerful and opened up a wide range of integration possibilities.

Using both APIs together, complex applications using Asterisk as the engine could be developed.

The Asterisk RESTful Interface (ARI) was created to address these concerns.

### ARI

While AMI is good at call control and AGI is good at allowing a remote process to execute dialplan applications, neither of these APIs was designed to let a developer build their own custom communications application. 

ARI is an asynchronous API that allows developers to build communications applications by exposing the raw primitive objects in Asterisk - channels, bridges, endpoints, media, etc. - through an intuitive REST interface.

The state of the objects being controlled by the user are conveyed via JSON events over a WebSocket.
