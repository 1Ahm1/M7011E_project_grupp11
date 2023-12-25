import { Component, inject } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {

  constructor(private router: Router) {}

  authService: AuthService = inject(AuthService);

  role: String = "customer";
  username: String = '';
  password: String = '';
  rePassword: String = '';
  name: String = '';
  passwordError: boolean = false;
  pendingUserId: number = 0;
  async register(): Promise<void>
  {
    
    if(this.password != this.rePassword)
    {
      this.passwordError = true;
    }
    else
    {
      try
      {
        const username = this.username;
        const password = this.password;
        const name = this.name;
        this.username = '';
        this.password = '';
        this.rePassword = '';
        const data = await this.authService.register(username, password, name, this.role)
        this.pendingUserId = data.pendingUserId;
        this.router.navigate(['activate-user/'])
        this.passwordError = false;
      }
      catch(e) {
        this.passwordError = true;
      }
    }
    
  }
}
