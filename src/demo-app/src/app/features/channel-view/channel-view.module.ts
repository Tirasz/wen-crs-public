import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ScrollingModule } from '@angular/cdk/scrolling';

import { ChannelViewRoutingModule } from './channel-view-routing.module';
import { ChannelViewComponent } from './channel-view.component';
import { CoreModule } from '../../core/core.module';
import { SharedModule } from '../../shared/shared.module';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';


@NgModule({
  declarations: [
    ChannelViewComponent
  ],
  imports: [
    CommonModule,
    ChannelViewRoutingModule,
    CoreModule,
    SharedModule,
    ScrollingModule,
    MatButtonModule,
    MatIconModule
  ]
})
export class ChannelViewModule { }
