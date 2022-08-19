% rebase('base.tpl', current_page = "Home page", note=note, error=error)
<section class="section has-background-white-bis">
    <div class="columns">
        <div class="column">
            <form action="/new_album/" method="POST">
                <div class="field">
                    <label class="label">Create new album:</label>
                    <div class="control has-icons-left">
                        <input class="input" name="new_album" type="text" placeholder="Album name...">
                        <span class="icon is-small is-left">
                            <i class="fa fa-book" aria-hidden="true"></i>
                        </span>
                    </div>
                    <div class="control">
                        <button class="button is-link has-background-grey-light">
                        Submit
                        </button>
                    </div>
                </div>
            </form>    
        </div>
        <div class="column">
            <form action="/upload_image/", method="POST", enctype="multipart/form-data">
                <b>Upload new photo:</b> <br/>                
                <input type="file" name="upload" />
                <input class="form-control" type="submit" value="upload" />
            </form>
        </div>
    </div>
</section>

<section class="section has-background-grey-lighter">
    % if len(list_of_albums)-account.num_friends_albums()!= 0:
    <b>Your albums:</b>
    <div class="column">
        % for album in list_of_albums:
        % if album.owner == account.username:
        % album_id = album.name+"."+album.owner
        <form action="/album/{{album_id}}" method="POST">
            <div class="field is-grouped">
                <div class="control">
                    <button class="button is-link has-background-grey-dark">
                    {{album.name}}
                    </button>
                </div>
            </div>
        </form>
        % end
        % end
    </div>
    % end
    % if account.num_friends_albums() != 0:
    <b>Friends' albums:</b>
    <div class="column">
        % for album in list_of_albums:
        % if album.owner != account.username:
        % album_id = album.name+"."+album.owner
        <div class="tile">
        <form action="/album/{{album_id}}" method="POST">
            <div class="field is-grouped">
                <div class="control">
                    <button class="button is-link has-background-white-bis">
                    {{album.name}}
                    </button>
                </div>
            </div>
        </form>
        % end
        % end
    </div>
    % end
</section>

<section class="section has-background-white-bis">
    % if account.images:
    <strong>Your images:</strong>
    % for image_id in account.images:
    <div class="tile">
        <article class="tile is-child box">
            <img src= "{{ get_url('database', filename= image_id) }}" class="img-fluid" />
            <form action="/add_to_album/{{image_id}}", method="POST">
                <div class="field">
                    <div class="control has-icons-left">
                        <input class="input" name="album_name" type="text" placeholder="Album name">
                        <span class="icon is-small is-left">
                            <i class="fa fa-book"></i>
                        </span>
                    </div>
                </div>
                <div class="field">
                    <div class="control has-icons-left">
                        <input class="input" name="album_owner" type="text" placeholder="Album admin">
                        <span class="icon is-small is-left">
                            <i class="fas fa-user"></i>
                        </span>
                    </div>
                </div>
                <div class="field is-grouped">
                    <div class="control">
                        <button class="button is-link has-background-grey-lighter">
                        Add to album
                        </button>
                    </div>
                </div>
            </form>
        </article>    
    </div> 
    % end
    % end
</section>