import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ScrollingModule } from '@angular/cdk/scrolling';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

import { PostViewRoutingModule } from './post-view-routing.module';
import { PostViewComponent } from './post-view.component';
import { SharedModule } from '../../shared/shared.module';


@NgModule({
  declarations: [
    PostViewComponent
  ],
  imports: [
    CommonModule,
    PostViewRoutingModule,
    SharedModule,
    ScrollingModule,
    MatButtonModule,
    MatIconModule
  ]
})
export class PostViewModule { }
