% rebase('base.tpl')
<p>{{username}}</p>
<form action="/log_out/" method="POST">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">Log out</button>
        </div>
    </div>
</form>

<form method="POST">
    <div class="field">
        <label class="label">Album name</label>
        <div class="control has-icons-left">
            <input class="input" name="new_album" type="text" placeholder="new_album">
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
<form action="/main_page/" enctype="multipart/form-data">
    Upload new photo: <input type="file" name="upload" />
    <input class="input" name="image_name" type="text" placeholder="image_name">
    <input class="form-control" type="submit" value="upload" />
</form>
<br>

#nastimaj da vsak album dobi gumb s svojim id!!!
%for album in username.albums:
<form action="/album/" method="get">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">album</button>
        </div>
    </div>
</form>
%end


%for image in username.images:
<form method="POST">
    <div class="field">
        <label class="label">album's name</label>
        <div class="control has-icons-left">
            <input class="input" name="album_name" type="text" placeholder="album's name">
            <span class="icon is-small is-left">
                <i class="fas fa-user"></i>
            </span>
        </div>
    </div>
    % if error:
    <p class="help is-danger">{{ error }}</p>
    % end
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">Add to album</button>
        </div>
    </div>
</form>


