/*
#www.lasselauch.com/lab/
#Use at your own risk
*/

(function() {
    try {
        app.beginUndoGroup("Copy Project to Watch-Folder");

        if (app.project.file) {
            app.project.save();
            var current_filename = app.project.file.name;
            var target_path = 'D:\\_CACHE\\_WatchFolder\\{filename}'.replace('{filename}', current_filename);
            var target = new File(target_path);
            var thisFile = new File(app.project.file.fsName);
            if (target.exists) {
                //whatever
            } else {
                thisFile.copy(target);
            }
        }

    } catch (err) {
        alert(err);
    } finally {
        app.endUndoGroup();
    }
})();
