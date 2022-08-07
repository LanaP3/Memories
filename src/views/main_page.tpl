% rebase('base.tpl')
<p>{{username.username}}</p>
<form action="/log_out/" method="POST">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">Log out</button>
        </div>
    </div>
</form>

<form method="POST">
    <div class="field">
        <label class="label">Create new album:</label>
        <div class="control has-icons-left">
            <input class="input" name="new_album" type="text" placeholder="album's name">
            <span class="icon is-small is-left">
                <i class="fas fa-user"></i>
            </span>
        </div>
        <div class="control">
            <button class="button is-link">New album</button>
        </div>
    </div>
</form>
<br>
<form action="/main_page/", method="POST", enctype="multipart/form-data">
    Upload new photo: <input type="file" name="upload" />
    <input class="form-control" type="submit" value="upload" />
</form>
<br>

%for album in username.albums:
<form action="/album/" method="get">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">{{album.name}}</button>
        </div>
    </div>
</form>
%end


%for image in username.images:
<div>
<img src= "{{ get_url('database', filename= image) }}" class="img-fluid" />
</div>
<form method="POST">
    <div class="field">
        <div class="control has-icons-left">
            <input class="input" name="album_name" type="text" placeholder="album's name">
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
%end

