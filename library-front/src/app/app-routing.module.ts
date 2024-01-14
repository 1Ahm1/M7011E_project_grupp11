import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { ActivateUserComponent } from './activate-user/activate-user.component';
import { BookListComponent } from './book-list/book-list.component';
import { BookDetailsComponent } from './book-details/book-details.component';
import { ProfileMenuComponent } from './profile-menu/profile-menu.component';
import { CustomerGuard, ManagerGuard, UserGuard, AdminGuard} from './auth-guard';
import { CartComponent } from './cart/cart.component';
import { LibraryComponent } from './library/library.component';
import { ProfileComponent } from './profile/profile.component';
import { CreateBookComponent } from './create-book/create-book.component';
import { AdminHomeComponent } from './admin-home/admin-home.component';
import { ManagerBookListComponent } from './manager-book-list/manager-book-list.component';
import { EditBookComponent } from './edit-book/edit-book.component';

const routes: Routes = [
  { path: 'home', component: BookListComponent, canActivate: [CustomerGuard] },
  { path: 'manager/create', component: CreateBookComponent, canActivate: [ManagerGuard] },
  { path: 'manager/home', component: ManagerBookListComponent, canActivate: [ManagerGuard] },
  { path: 'manager/book/:bookId', component: EditBookComponent, canActivate: [ManagerGuard] },
  { path: 'profile', component: ProfileComponent, canActivate: [UserGuard] },
  { path: 'cart', component: CartComponent, canActivate: [CustomerGuard] },
  { path: 'library', component: LibraryComponent, canActivate: [CustomerGuard] },
  { path: '', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'activate-user', component: ActivateUserComponent },
  { path: 'book/:bookId', component: BookDetailsComponent, canActivate: [CustomerGuard]},
  { path: 'admin/home', component: AdminHomeComponent, canActivate: [AdminGuard]}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
