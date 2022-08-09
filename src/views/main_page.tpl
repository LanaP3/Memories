% rebase('base.tpl', current_page = "Home page")
<p>{{account.username}}</p>


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
<form action="/main_page/", method="POST", enctype="multipart/form-data">
    Upload new photo: <input type="file" name="upload" />
    <input class="form-control" type="submit" value="upload" />
</form>
<br>

%for album in account.albums:
%if album.owner == account.username:
<form action="/album/{{album.name}}" method="POST">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">{{album.name}}</button>
        </div>
    </div>
</form>
%else:
<strong>Friends' albums:</strong>
<p>"{{album.owner}}'s album:"</p>
<form action="/album/{{album.name}}" method="POST">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">{{album.name}}</button>
        </div>
    </div>
</form>
%end
%end


%for image in account.images:
<div>
<img src= "{{ get_url('database', filename= image) }}" class="img-fluid" />
</div>
<form action="/add_to_album/", method="POST">
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

