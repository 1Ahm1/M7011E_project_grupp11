import { Component, inject } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { UserProfile } from '../interfaces/entities';

@Component({
  selector: 'app-profile-menu',
  templateUrl: './profile-menu.component.html',
  styleUrls: ['./profile-menu.component.css']
})
export class ProfileMenuComponent {

  authService: AuthService = inject(AuthService);

  constructor() {
    this.profile = null;
    this.authService.profile$.subscribe((profile) => {
      this.profile = profile;
     });
    if(this.profile == null)
    {
      this.getProfile();
    }
  }

  profile: UserProfile | null;

  async getProfile() {
    this.profile = await this.authService.getProfile();

  }
  
}
