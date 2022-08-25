% rebase('base.tpl', current_page=album.name, error=error)


<form action="/remove_album/" method="POST">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link has-background-grey-light	">
            <i class="fa-solid fa-trash"></i>
            % if account.username==album.owner:
            <sub>DELETE ALBUM</sub>
            % else:
            <sub>LEAVE ALBUM</sub>
            % end
            </button>
        </div>
    </div>
</form>

<div class="tile is-ancestor">
    <article class="tile is-child box">
        <div>
        <b>ALBUM NAME:</b>  {{album.name}}<br/>
        <b>ADMIN:</b>  {{album.owner}}<br/>
        <b>DATE:</b>  {{album.date_added}}<br/>
        <b>PEOPLE:</b>  {{str_of_people}}
        </div>

        % if account.username==album.owner:
        <form action="/add_friend/" method="POST">
            <div class="field">
                <div class="control has-icons-left">
                    <input class="input" name="friend" type="text" placeholder="friend's name">
                    <span class="icon is-small is-left">
                        <i class="fas fa-user"></i>
                    </span>
                </div>
            </div>
            <div class="field is-grouped">
                <div class="control">
                    <button class="button is-link is-outlined">
                    add friend
                    </button>
                </div>
            </div>
        </form>
        % end
    </article>
</div>

<section class="section has-background-white-bis">
    <div class="columns">
        % from model import sort_in_columns
        % from model import Picture
        % for i in range(4):
        % images = sort_in_columns(list(album.images),4,i)
        <div class="column">

            % for image_id in images:
            % image = Picture(image_id, album.id)
            <div class="box">
                <img src= "{{ get_url('database', filename= image_id) }}" class="img-fluid" />
                <footer class="card-footer">    
                    <a class="card-footer-item", href="/image/{{image_id}}">
                        <i class="fa fa-bars" aria-hidden="true"></i>
                    </a>
                    <div class="card-footer-item">
                        % if len(image.likes) + len(image.dislikes) == 0:
                        <progress class="progress is-danger" value=1 max=2></progress>
                        % else:
                        <progress class="progress is-danger" value={{len(image.likes)}} max={{len(image.likes)+len(image.dislikes)}}></progress>
                        % end
                        {{len(image.likes)}}<i class="fa-regular fa-heart"></i>
                    </div>
                    % if account.username == album.owner:
                    <a class="card-footer-item", href="/delete_image/{{image_id}}">
                        <i class="fa-solid fa-trash"></i>
                    </a>
                    % end
                </footer>
            </div>
            % end
        </div>
        % end
    </div>
</section>