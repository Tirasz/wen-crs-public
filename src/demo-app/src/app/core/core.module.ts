import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { ChannelListComponent } from './components/channel-list/channel-list.component';
import { SharedModule } from '../shared/shared.module';
import { DummyClientService } from './services/dummy-client.service';
import { ElasticClientService } from './services/elastic-client.service';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';


@NgModule({
  declarations: [
    ChannelListComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    HttpClientModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule
  ],
  exports: [
    ChannelListComponent
  ],
  providers: [
    DummyClientService,
    ElasticClientService
  ]
})
export class CoreModule { }
