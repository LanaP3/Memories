% rebase('base.tpl', current_page = "Home page", note = note)

% if error:
<p class="help is-danger">{{error}}</p>
% end
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
    <b>Upload new photo:</b> <br/>
    <input type="file" name="upload" />
    <input class="form-control" type="submit" value="upload" />
</form>
<br>
% if len(list_of_albums)-account.num_friends_albums()!= 0:
<b>Your albums:</b>
% for album in list_of_albums:
% if album.owner == account.username:
% album_id = album.name+"."+album.owner
<form action="/album/{{album_id}}" method="POST">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">{{album.name}}</button>
        </div>
    </div>
</form>
% end
% end
% end

% if account.num_friends_albums() != 0:
<b>Friends' albums:</b>
% end
% for album in list_of_albums:
% if album.owner != account.username:
% album_id = album.name+"."+album.owner
<form action="/album/{{album_id}}" method="POST">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">{{album.name}}</button>
        </div>
    </div>
</form>
% end
% end


% if account.images:
<strong>Your images:</strong>
% end
% for image_id in account.images:

<div>
<img src= "{{ get_url('database', filename= image_id) }}" class="img-fluid" />
</div>
<form action="/add_to_album/{{image_id}}", method="POST">
    <div class="field">
        <div class="control has-icons-left">
            <input class="input" name="album_name" type="text" placeholder="album's name">
            <span class="icon is-small is-left">
                <i class="fa fa-book"></i>
            </span>
        </div>
    </div>
    <div class="field">
        <div class="control has-icons-left">
            <input class="input" name="album_owner" type="text" placeholder="album's creator">
            <span class="icon is-small is-left">
                <i class="fas fa-user"></i>
            </span>
        </div>
    </div>
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">Add to album</button>
        </div>
    </div>
</form>
% end

