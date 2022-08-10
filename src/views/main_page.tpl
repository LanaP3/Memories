% rebase('base.tpl', current_page = "Home page")


<form action="/new_album/" method="POST">
    <div class="field">
        <label class="label">Create new album:</label>
        <div class="control has-icons-left">
            <input class="input" name="new_album" type="text" placeholder="album's name">
            <span class="icon is-small is-left">
                <i class="fa fa-book" aria-hidden="true"></i>
            </span>
        </div>
        <div class="control">
            <button class="button is-link">New album</button>
        </div>
    </div>
</form>
<br>
<form action="/upload_image/", method="POST", enctype="multipart/form-data">
    Upload new photo: <input type="file" name="upload" />
    <input class="form-control" type="submit" value="upload" />
</form>
<br>

%for album in list_of_albums:
%if album.owner == account.username:
<form action="/album/{{album.name}}" method="POST">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">{{album.name}}</button>
        </div>
    </div>
</form>
%end
%end

<strong>Friends' albums:</strong>
%for album in list_of_albums:
%if album.owner != account.username:
<form action="/album/{{album.name}}" method="POST">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">{{album.name}}</button>
        </div>
    </div>
</form>
%end
%end


%if account.images:
<strong>Your images:</strong>
%end
%for image_id in account.images:
<div>
<img src= "{{ get_url('database', filename= image_id) }}" class="img-fluid" />
</div>
<form action="/add_to_album/{{image_id}}", method="POST">
    <div class="field">
        <div class="control has-icons-left">
            <input class="input" name="album_name" type="text" placeholder="album's name">
            <span class="icon is-small is-left">
                <i class="fa fa-book" aria-hidden="true"></i>
            </span>
        </div>
    </div>
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">Add to album</button>
        </div>
    </div>
</form>
%end

