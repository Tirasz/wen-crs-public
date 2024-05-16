import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { Post } from '../../../core/services/types';

@Component({
  selector: 'app-post-list-item',
  templateUrl: './post-list-item.component.html',
  styleUrls: ['./post-list-item.component.scss']
})
export class PostListItemComponent {
  @Input() post: Post;
  @Output() clicked = new EventEmitter<Post>();
  onClick() {
    this.clicked.emit(this.post);
  }
  constructor() { }
}
