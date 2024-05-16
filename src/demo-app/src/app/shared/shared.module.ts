import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatSliderModule } from '@angular/material/slider';
import { MarkdownModule } from 'ngx-markdown';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';

import { ChannelListItemComponent } from './components/channel-list-item/channel-list-item.component';
import { PostListItemComponent } from './components/post-list-item/post-list-item.component';
import { PostViewHeaderComponent } from './components/post-view-header/post-view-header.component';



@NgModule({
  declarations: [
    ChannelListItemComponent,
    PostListItemComponent,
    PostViewHeaderComponent,
  ],
  imports: [
    CommonModule,
    MarkdownModule,
    MatButtonToggleModule,
    MatSliderModule,
    MatProgressSpinnerModule,
    MatSlideToggleModule
  ],
  exports: [
    ChannelListItemComponent,
    PostListItemComponent,
    PostViewHeaderComponent
  ]
})
export class SharedModule { }
