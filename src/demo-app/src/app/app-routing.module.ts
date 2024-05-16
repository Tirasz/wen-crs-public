import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  { path: 'channel-view', loadChildren: () => import('./features/channel-view/channel-view.module').then(m => m.ChannelViewModule) },
  { path: 'post-view', loadChildren: () => import('./features/post-view/post-view.module').then(m => m.PostViewModule) },
  { path: '**', loadChildren: () => import('./features/home/home.module').then(m => m.HomeModule) }];

@NgModule({
  imports: [RouterModule.forRoot(routes, { bindToComponentInputs: true })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
