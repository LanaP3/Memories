% rebase('base.tpl', current_page = "image", note=None, error=None)
<div class="columns is-centered">
  <div class="column is-one-third">
        <div class = "card">
            <div class="card-image">
                <figure class="image">
                    <img src="{{ get_url('database', filename= image.id) }}" >
                </figure>
            </div>
            <footer class="card-footer">
                % if account.username in image.likes:
                <a class="card-footer-item has-background-grey" href="/like/">
                    like &nbsp; <i class="fa-regular fa-heart"></i>
                </a>
                <a class="card-footer-item" href="/dislike/">
                    dislike &nbsp; <i class="fa-solid fa-xmark"></i>
                </a>
                
                % elif account.username in image.dislikes:
                <a class="card-footer-item" href="/like/">
                    like &nbsp; <i class="fa-regular fa-heart"></i>
                </a>
                <a class="card-footer-item has-background-grey" href="/dislike/">
                    dislike &nbsp; <i class="fa-solid fa-xmark"></i>
                </a>
                
                % else:
                <a class="card-footer-item" href="/like/">
                    like &nbsp; <i class="fa-regular fa-heart"></i>
                </a>
                <a class="card-footer-item" href="/dislike/">
                    dislike &nbsp; <i class="fa-solid fa-xmark"></i>
                </a>
                % end

                <div class="card-footer-item" href="/like/">
                    % if len(image.likes) + len(image.dislikes) == 0:
                    <progress class="progress is-danger" value=1 max=2></progress>
                    % else:
                    <progress class="progress is-danger" value={{len(image.likes)}} max={{len(image.likes)+len(image.dislikes)}}></progress>
                    % end
                    {{len(image.likes)}}<i class="fa-regular fa-heart"></i>
                </div>
            </footer>
        </div>
        <div class = "tile box"
            <article class = "media">
                <div class = "media-content">
                   <div class = "content">
                        %for comment in image.comments:                    
                        <strong>{{comment[0]}}</strong>
                        <br>
                        <p>
                        {{comment[1]}}
                        </p>
                        %end
                    </div>
                    <form action="/add_comment/" method="POST">
                        <div class="field">
                            <div class="control has-icons-left">
                                <input class="input" name="comment" type="text" placeholder="Add a comment...">
                                <span class="icon is-small is-left">
                                    <i class="fa fa-pencil"></i>
                                </span>
                            </div>
                        </div>
                        <div class="field is-grouped">
                            <div class="control">
                                <button class="button is-link is-outlined">Submit</button>
                            </div>
                        </div>
                    </form>
                </div>
            </article>
        </div>
    </div>
</div>

  