import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ChannelViewComponent } from './channel-view.component';

const routes: Routes = [{ path: '', component: ChannelViewComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ChannelViewRoutingModule { }
