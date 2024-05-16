import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { Channel } from '../../../core/services/types';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-channel-list-item',
  templateUrl: './channel-list-item.component.html',
  styleUrls: ['./channel-list-item.component.scss']
})
export class ChannelListItemComponent implements OnChanges {
  @Input() channel: Channel;
  @Output() clicked = new EventEmitter<Channel>()

  imageSrc = "";

  onClick() {
    this.clicked.emit(this.channel);
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.setImg();
  }

  setImg() {
    if (this.channel) {
      const seed = this.channel.id.replace(/\//g, '');
      this.imageSrc = "https://picsum.photos/seed/" + seed + "/100";
    }
  }

  constructor(private http: HttpClient, private router: Router) { }

}
