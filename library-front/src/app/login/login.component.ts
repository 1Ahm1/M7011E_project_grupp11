import { Component, inject } from '@angular/core';
import { LoginData } from '../interfaces/entities';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {

  authService: AuthService = inject(AuthService);

  constructor(private router: Router) { 
    if(this.authService.isAuthenticated())
    {
      if(this.authService.getRole() === 'customer')
        this.router.navigate(['home/']);
      else if(this.authService.getRole() === 'manager')
        this.router.navigate(['manager/home/']);
      else
        this.router.navigate(['admin/home/']);
    }
  }

  username: String = '';
  password: String = '';

  loginError: boolean = false;

  async login(): Promise<void> {
    
    try
    {
      const username = this.username;
      const password = this.password;
      this.username = '';
      this.password = '';
      const loginData: LoginData = await this.authService.login(username, password)
      this.loginError = false;
      if(loginData.userProfile.defaultRole == 'customer')
        this.router.navigate(['home/']);
      else if(loginData.userProfile.defaultRole == 'manager')
        this.router.navigate(['manager/home/']);
      else
        this.router.navigate(['admin/home/']);
    }
    catch(e) {
      this.loginError = true;
    }
    
  }
}
