import { Injectable } from '@angular/core';
import { BASE_URL } from 'src/utils/configs';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import { LoginData, UserProfile } from '../interfaces/entities';
import { LoginRequest, RegisterRequest, ValidateUserRequest, RefreshTokenRequest, UpdateProfileRequest } from '../interfaces/requests';
import { RegisterData } from '../interfaces/entities';
import { Router } from '@angular/router';
import { delay, BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private localStorageKey = 'authState';
  private localAccessTokenKey = 'accessToken';
  private localRefreshTokenKey = 'refreshToken';
  private localRoleKey = 'role';

  username: String = '';
  password: String = '';
  pendingUserId: number = 0;
  role: String = '';
  accessToken: String = '';
  refreshToken: String = '';
  private isLoggedIn: boolean = false;
  
  private profile = new BehaviorSubject<UserProfile | null>(null);

  get profile$() {
    return this.profile.asObservable();
  }
  constructor(private http: HttpClient, private router: Router) { 
    
  }
  async ngOnInit() {
    const storedValue = localStorage.getItem(this.localStorageKey);
    this.isLoggedIn = storedValue !== null && JSON.parse(storedValue);
    this.accessToken = await this.getAccessToken();
    this.refreshToken = this.getRefreshToken();
    this.role = this.getRole();
  }
  async login(username: String, password: String): Promise<LoginData> {

    const loginUrl = BASE_URL + 'auth/token/';
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    const requestBody: LoginRequest = {
      email: username,
      password: password
    };


    let response = await this.http.post<any>(loginUrl, requestBody, { headers: headers }).toPromise();
    if(response.code == 200)
    {
      response = response.result;
      const loginData: LoginData = {
        accessToken: response.access_token,
        refreshToken:  response.refresh_token,
        userProfile : {
          userId: response.user_profile.user_id,
          email: response.user_profile.email,
          phoneNumber: response.user_profile.phone_number,
          name: response.user_profile.name,
          defaultLang: response.user_profile.default_lang,
          defaultRole: response.user_profile.default_role,
          imageUrl: response.user_profile.image_url
        }
      };
      this.accessToken = loginData.accessToken;
      this.refreshToken = loginData.refreshToken;
      this.isLoggedIn = true;
      this.role = loginData.userProfile.defaultRole;
      localStorage.setItem(this.localStorageKey, JSON.stringify(this.isLoggedIn));
      localStorage.setItem(this.localAccessTokenKey, JSON.stringify(this.accessToken));
      localStorage.setItem(this.localRefreshTokenKey, JSON.stringify(this.refreshToken));
      localStorage.setItem(this.localRoleKey, JSON.stringify(this.role));
      this.profile.next(loginData.userProfile);
      return loginData;
    } 
    else
    {
      throw new Error();
    }
  }

  async register(username: String, password: String, name: String, role: String): Promise<RegisterData> {

    const registerUrl = BASE_URL + 'auth/register/';
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    const requestBody: RegisterRequest = {
      email: username,
      password: password,
      role: role,
      name: name
    };

    let response = await this.http.post<any>(registerUrl, requestBody, { headers: headers }).toPromise();
    if(response.code == 200)
    {
      response = response.result;
      const registerData: RegisterData = {
        pendingUserId: response.pending_user_id
      };
      this.username = username;
      this.password = password;
      this.pendingUserId = registerData.pendingUserId;
      this.role = role;
      localStorage.setItem(this.localRoleKey, JSON.stringify(this.role));

      return registerData;
    } 
    else
    {
      throw new Error();
    }
  }

  async validateUser(validationCode: number): Promise<LoginData> {

    const validateUrl = BASE_URL + 'auth/activate-user/';
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    const requestBody: ValidateUserRequest = {
      email: this.username,
      pending_user_id: this.pendingUserId,
      role: this.getRole(),
      validation_code: validationCode
    };

    let response = await this.http.post<any>(validateUrl, requestBody, { headers: headers }).toPromise();
    if(response.code == 200)
    {
      response = response.result;
      const loginData: LoginData = {
        accessToken: response.access_token,
        refreshToken:  response.refresh_token,
        userProfile : {
          userId: response.user_profile.user_id,
          email: response.user_profile.email,
          phoneNumber: response.user_profile.phone_number,
          name: response.user_profile.name,
          defaultLang: response.user_profile.default_lang,
          defaultRole: response.user_profile.default_role,
          imageUrl: response.user_profile.image_url
        }
      };
      this.accessToken = loginData.accessToken;
      this.refreshToken = loginData.refreshToken;
      this.isLoggedIn = true;
      this.role = loginData.userProfile.defaultRole;
      localStorage.setItem(this.localStorageKey, JSON.stringify(this.isLoggedIn));
      localStorage.setItem(this.localAccessTokenKey, JSON.stringify(this.accessToken));
      localStorage.setItem(this.localRefreshTokenKey, JSON.stringify(this.refreshToken));
      localStorage.setItem(this.localRoleKey, JSON.stringify(this.role));
      this.profile.next(loginData.userProfile);
      return loginData;
    } 
    else
    {
      throw new Error();
    }
  }

  getAccessToken(): String {
    const storedValue = localStorage.getItem(this.localAccessTokenKey);
    if(storedValue != null) this.accessToken = JSON.parse(storedValue);
    if(this.accessToken == '') this.refreshAccessToken();
    return this.accessToken;
  }

  getRole(): String {
    const storedValue = localStorage.getItem(this.localRoleKey);
    if(storedValue != null) this.role = JSON.parse(storedValue);
    return this.role;
  }

  getRefreshToken(): String {
    const storedValue = localStorage.getItem(this.localRefreshTokenKey);
    if(storedValue != null) this.refreshToken = JSON.parse(storedValue);
    if(this.refreshToken == '')
    {
      this.isLoggedIn = false;
      localStorage.setItem(this.localStorageKey, JSON.stringify(this.isLoggedIn));      
    }
    return this.refreshToken;
  }

  async refreshAccessToken(): Promise<void> {
    const refreshTokenUrl = BASE_URL + 'auth/refresh/';
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    const requestBody: RefreshTokenRequest = {
      refresh_token: this.getRefreshToken(),
      role: this.getRole()
    };

    let response = await this.http.post<any>(refreshTokenUrl, requestBody, { headers: headers }).toPromise();
    if(response.code == 200)
    {
      response = response.result;
      this.accessToken = response.access_token;
      localStorage.setItem(this.localAccessTokenKey, JSON.stringify(this.accessToken));
    } 
    else
    {
      this.isLoggedIn = false;
      localStorage.setItem(this.localStorageKey, JSON.stringify(this.isLoggedIn));   
      this.router.navigate(['/']);   
    }
  }
  isAuthenticated(): boolean {
    const storedValue = localStorage.getItem(this.localStorageKey);
    this.isLoggedIn = storedValue !== null && JSON.parse(storedValue);
    return this.isLoggedIn;
  }

  logout() {
    this.isLoggedIn = false;
    this.accessToken = '';
    this.refreshToken = '';
    this.username = '';
    this.role = '';
    this.password = '';
    this.pendingUserId = 0;
    localStorage.clear();

    this.router.navigate(['/']);
  }

  async handleResponse(response: any) {
    if(response.code == 200)
    {
    }
    else if(response.code == 401)
    {
      console.log('refreshing access token');
      this.refreshAccessToken();
    }
    else
    {
      throw new Error();
    }
    
  }

  async getProfile(): Promise<UserProfile> {
    const getProfileUrl = BASE_URL + 'user/profile/get/';
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-Token': this.getAccessToken().toString()
    });

    let response = await this.http.get<any>(getProfileUrl, { headers: headers }).toPromise();
    await this.handleResponse(response);
    const profile: UserProfile = {
      userId: response.result.user_id,
      email: response.result.email,
      phoneNumber: response.result.phone_number,
      defaultLang: response.result.default_lang,
      defaultRole: response.result.default_role,
      name: response.result.name,
      imageUrl: response.result.image_url
    }
    return profile;

  }
  async updateProfile(name: String): Promise<void> {
    const updateProfileUrl = BASE_URL + 'user/profile/update/';
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-Token': this.getAccessToken().toString()
    });

    const requestBody: UpdateProfileRequest = {
      name: name

    };
    let response = await this.http.post<any>(updateProfileUrl, requestBody, { headers: headers }).toPromise();
    await this.handleResponse(response);
    const newProfile: UserProfile = await this.getProfile();
    this.profile.next(newProfile);

  }
}
