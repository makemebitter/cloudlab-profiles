#### Use GPU machines on CloudLab

##### Overview

CloudLab is a meta-cloud that provides bare metal machines for experimenting and development.

You can request a slice of machines and other resources like storage and networking; this is called an experiment. The configuration of an experiment is called profile and profiles can be shared with other users. A profile is defined in GENI RSpecs. Details are in [CloudLab Manual](https://docs.cloudlab.us/cloudlab-manual.html).

As of June 2020, GPU machines are only available in Wisconsin and Clemson cluster. You can find the details [Here](https://docs.cloudlab.us/cloudlab-manual.html#%28part._hardware%29).

##### 1. Register a CloudLab account

##### 2. Upload your SSH key to CloudLab
From your portal at the upper right corner, click your user name -> Manage SSH Keys.

##### 3. Reserve GPU nodes

The GPU resources are heavily contested and it is better to reserve the nodes before-hand (~1 week ahead is OK). To do so, from your portal, click Experiments -> Reserve Nodes.

##### 4. Start an experiment
There are lots of pre-defined profiles and you can use one to instantiate your cluster. Note not all of them are easy to use and most are bundled with some specific softwares. 
You can use my clean profile named ```cluster-select-hardware```. It allows you to select hardwares for your master and slave nodes and setup the network interfaces.
From your portal, click Experiments -> Start Experiment -> Change Profile -> choose the profile listed above.
Then specify the parameters, choose the harware types to your reserved node types or leave it as-is if you just want to play with it.
Click next and select the cluster location, has to be the same as your nodes.
All experiments are created with a 16 hrs time limit, you can extend it later.

##### 5. Log into your nodes via SSH
In the experiment's page, select List View tab to show all the IP addresses of your nodes. You can then log into them and install softwares you need like CUDA, tensorflow/pytorch, celery ...
##### 6. Install and use Celery

I recommend reading and following the [official guide](https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html) of Celery step-by-step.

##### 7. Install and use Cerebro-Standalone

Cerebro is our research project and the standalone version is not publicly available yet. If you are interested and want to give it a try, please contact me and I can send you a WIP version.

##### 8. Create your own profile with bootstrap scripts

It is highly recommended that you maintain your own profile so that you don't have to re-install everything each time you delete your nodes. You can use mine as a start. [Link](https://github.com/makemebitter/cloudlab-profiles) Within the repo, ```profile.py``` is the CloudLab profile config file that handles the resources requests. Within it also registers a bootstrap task which executes ```bootstap.sh``` that is colocated in the repo. You can fork the repo and add your own bootsraping scripts to ```bootstap.sh```, and later import the profile to CloudLab.

##### Caveats
The nodes instantiated usually come with two network interfaces; a public one called control net and a private one called experiment net. Remember to carefully deploy your networking-intensive applications to the **private** one otherwise CloudLab will ask questions and suspend your account.







