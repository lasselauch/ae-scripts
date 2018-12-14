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
            var thisFile = new File(app.project.file.fsName); // (of fsname - look it up)
            if (target.exists) {
                //put stuff in here to increment file name using regex, perhaps
                //or save the file elsewhere.
            } else {
                thisFile.copy(target);
            }
            //alert(app.project.file.fsName);
        }

    } catch (err) {
        alert(err);
    } finally {
        app.endUndoGroup();
    }
})();
