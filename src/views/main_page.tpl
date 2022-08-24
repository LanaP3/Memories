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
                <div class="file">
                    <label class="file-label">
                        <input class="file-input" type="file" name="upload">
                        <span class="file-cta">
                            <span class="file-icon">
                                <i class="fas fa-upload"></i>
                            </span>
                            <span class="file-label">
                                Choose a file…
                            </span>
                        </span>
                    </label>
                </div>
                <div class="control">
                    <button class="button is-link has-background-grey-light">
                        Submit
                    </button>
                </div>
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
            
            <form action="/add_to_album/{{image_id}}" method="POST">
                <div class="field">
                    <div class="control">
                        <div class="select">
                            <select name="album_id">
                                <option value="">
                                    Choose an album
                                </option>
                                % for album in list_of_albums:
                                % if album.owner == account.username:
                                <option value={{album.id}}>
                                    {{album.name}}
                                </option>
                                % end
                                % end
                                % if account.num_friends_albums() != 0:

                                % for album in list_of_albums:
                                % if album.owner != account.username:
                                <option value={{album.id}}>
                                    {{album.name}} by {{album.owner}}
                                </option>  
                                % end
                                % end
                                % end
                                </div>
                            </select>
                        </div>
                    </div>   
                </div>   
                <div class="field has-addons">
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