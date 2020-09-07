## 标注存储的Git集成

### 说明

该应用程序允许集成任何git存储库，比如CVAT任务的注释存储。
它支持github或gitlab存储库。
SSH协议用于授权。

### Using

  * Put a private SSH key into the ```ssh``` directory. The public key corresponding to this private key should be attached to an github user.
  * If you don't put any custom key, it will generated automatically.
  * Setup a repository URL and a path (which is relative for a repository) in the create task dialog.
  * Annotate a task.
  * Press the button "Git Repository Sync" on the dashboard.
  * In the dialog window press the button "Sync" and waiting for some time.
  * An annotation will be dumped, archived and pushed to the attached remote repository. You can do a pull request manually.
