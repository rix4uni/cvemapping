extern crate ring;
extern crate crypto;
#[macro_use]
extern crate log;
extern crate env_logger;

use ring::{digest, hmac, pbkdf2};
use crypto::aes;
use crypto::buffer::{WriteBuffer, ReadBuffer, BufferResult};

#[derive(Debug)]
struct Encryption {
    serial_num: Vec<u8>,
    iv: Vec<u8>,
    hmac: Vec<u8>,
    keys: Vec<u8>,
}

/// Structure of DataSet:
/// msg + sha256(msg)[:4] + padding
/// all DataSet encrypted by AES (see Encryption)
#[derive(Debug)]
struct DataSet {
    data_type: u8,
    sent_len: u8,
    sha256sum: Vec<u8>,
    msg: Vec<u8>,
}

/// Ack type of response.
#[derive(Debug)]
struct Ack {
    type_resp: u8,
    data: Vec<u8>,
}

impl Ack {
    fn new<S: AsRef<str>>(ack_str: S) -> Result<Self, String> {
        let mut ack_num: Vec<u8> = Vec::new();
        for dig in ack_str.as_ref().split_whitespace() {
            ack_num.push(u8::from_str_radix(dig, 16)
                         .map_err(|err| err.to_string())?);
        }
        let data_len = ack_num.get(1)
            .map(|x| x.clone() as usize)
            .ok_or("AckError: getting len")?;

        Ok(
            Ack {
                type_resp: 0x04,
                data: ack_num.get(2..data_len + 2)
                    .map(|x| Vec::from(x))
                    .ok_or("AckError: getting data")?,
            }
        )
    }

    fn get_data(&self) -> &Vec<u8> {
        &self.data
    }
}

impl DataSet {
    fn new<S: AsRef<str>>(data_type: u8, msg: S) -> Self {
        let mut msg_vec: Vec<u8> = Vec::new();
        msg_vec.extend_from_slice(msg.as_ref().as_bytes());

        DataSet {
            data_type: data_type,
            sent_len: 0,
            sha256sum: digest::digest(&digest::SHA256, &msg_vec).as_ref().to_owned(),
            msg: msg_vec,
        }
    }

    fn get_encrypted_data(&self, encryptor: &Encryption) -> Result<Vec<u8>, String> {
        let mut data: Vec<u8> = Vec::from(self.msg.as_slice());

        let sha256sum_4 = self.sha256sum.as_slice()
            .get(0..4)
            .ok_or("Error: getting sha256 of message")?;
        debug!("sha256sum[0:4]: {:?}", sha256sum_4);
        data.extend(sha256sum_4);

        // let padding = get_padding(&data);
        // data.extend(padding);

        debug!("Data before encrypting (w/o padding): {:?}", data);

        let mut final_result = Vec::<u8>::new();
        loop {
            debug!("test before cbc_enc");
            let mut encryptor = aes::cbc_encryptor(aes::KeySize::KeySize128,
                                                   &encryptor.keys,
                                                   &encryptor.iv,
                                                   crypto::blockmodes::PkcsPadding);

            debug!("test");
            let mut readbuffer = crypto::buffer::RefReadBuffer::new(&data);
            let mut buffer = [0; 4096];
            let mut writebuffer = crypto::buffer::RefWriteBuffer::new(&mut buffer);
            let result = encryptor.encrypt(&mut readbuffer, &mut writebuffer, true)
                .or(Err("DataSetError: encrypting message"))?;
            debug!("test after encrypt");
            final_result.extend(writebuffer
                                .take_read_buffer()
                                .take_remaining()
                                .iter()
                                .map(|&i| i));

            match result {
                BufferResult::BufferUnderflow => break,
                BufferResult::BufferOverflow => { }
            }
        }
        debug!("Data after encrypting: {:?}", final_result);

        Ok(final_result)
    }
}

impl Encryption {
    fn new<S: AsRef<str>>(serial_num: S, ack_unlock: &Ack) -> Result<Self, String> {
        let mut keys: Vec<u8> = Vec::new();
        let serial_num: Vec<u8> = serial_num.as_ref().to_owned().into_bytes();
        let iv: Vec<u8> = ack_unlock.get_data().to_owned();

        pbkdf2::derive(&digest::SHA256, 1000, &iv, &serial_num, &mut keys);
        Ok(
            Encryption {
                serial_num: serial_num,
                iv: iv,
                hmac: Vec::with_capacity(16),
                keys: keys,
            }
        )
    }

    fn generate_hmac(&mut self) {
        let sign_key = hmac::SigningKey::new(&digest::SHA256, &self.iv);
        let sign = hmac::sign(&sign_key, &self.serial_num);
        let sign_ref = sign.as_ref();

        self.hmac.extend_from_slice(sign_ref.get(sign_ref.len() - 16 ..).unwrap());
    }

    fn generate_derived_keys(&mut self) {
        pbkdf2::derive(&digest::SHA256, 1000, &self.iv, &self.serial_num, &mut self.keys);
        debug!("keys: {:?}", self.keys);
        debug!("iv: {:?}", self.iv);
    }

    fn print_hmac_query(&self) {
        print!("0x{:02x} 0x{:02x}", 6, 16); // NONCE query type + length of data
        for i in &self.hmac {
            print!(" 0x{:02x}", i);
        }
        println!();
    }

    fn print_derived_keys(&self) {
        for i in &self.keys {
            print!("{:x} ", i);
        }
    }
}

fn get_padding(data: &[u8]) -> Vec<u8> {
    let mut padding: Vec<u8> = Vec::new();
    let length: u8 = 16 - (data.len() % 16) as u8;
    for _i in 0..length {
        padding.push(length);
    }
    debug!("padding: {:?}", padding);
    padding
}

fn main() {
    env_logger::init();

    let args: Vec<String> = std::env::args().collect();
    if args.len() != 5 {
        println!("Usage: {} 6_DIGITS_OF_SERIAL_NUMBER ACK_UNLOCK SETTING_TYPE COMMAND", args[0]);
        std::process::exit(1);
    };

    let serial_number: String = args.get(1).unwrap().to_owned();
    let ack_unlock: Ack = Ack::new(args.get(2).unwrap()).expect("Wrong ACK_UNLOCK");
    let setting_type: u8 = args.get(3).unwrap().parse().expect("Wrong SETTING_TYPE");
    let command: String = args.get(4).unwrap().to_owned();


    debug!("[+] serial number: {}", serial_number);
    debug!("[+] ack_unlock: {:?}", ack_unlock);
    debug!("[+] setting_type: {}", setting_type);
    debug!("[+] command: {}", command);

    let mut enc = Encryption::new(serial_number, &ack_unlock).unwrap();
    enc.generate_hmac();
    enc.print_hmac_query();
    enc.generate_derived_keys();
    // enc.print_derived_keys();
    debug!("{:?}", enc);

    let data = DataSet::new(setting_type, command);
    debug!("{:?}", data);
    for x in data.get_encrypted_data(&enc).unwrap() {
        print!("0x{:02x} ", x);
    }
    println!();
    enc.print_hmac_query();
}
